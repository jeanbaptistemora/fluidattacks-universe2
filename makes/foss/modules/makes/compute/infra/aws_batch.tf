data "aws_ec2_instance_type" "instance" {
  instance_type = "c5ad.xlarge"
}

resource "aws_subnet" "default" {
  availability_zone       = "${var.region}a"
  cidr_block              = "192.168.8.0/23"
  map_public_ip_on_launch = true
  vpc_id                  = var.batch_vpc_id

  tags = {
    "Name"            = "batch"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_role" "aws_ecs_instance_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      }, {
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "spotfleet.amazonaws.com"
      }
    }]
  })
  name = "aws_ecs_instance_role"

  tags = {
    "Name"            = "aws_ecs_instance_role"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_role_policy_attachment" "aws_ecs_instance_role" {
  role       = aws_iam_role.aws_ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_role_policy_attachment" "aws_ecs_instance_role_fleet_tagging" {
  role       = aws_iam_role.aws_ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2SpotFleetTaggingRole"
}

resource "aws_iam_instance_profile" "aws_ecs_instance_role" {
  name = "aws_ecs_instance_role"
  role = aws_iam_role.aws_ecs_instance_role.name
}

resource "aws_iam_role" "aws_batch_service_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "batch.amazonaws.com"
      }
    }]
  })
  name = "aws_batch_service_role"

  tags = {
    "Name"            = "aws_batch_service_role"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_role_policy_attachment" "aws_batch_service_role" {
  role       = aws_iam_role.aws_batch_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_security_group" "aws_batch_compute_environment_security_group" {
  name   = "aws_batch_compute_environment_security_group"
  vpc_id = var.batch_vpc_id

  # AWS manage this things and it's unknown what source port, protocol or ip
  # will access the machine
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name"            = "aws_batch_compute_environment_security_group"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_launch_template" "batch_instance_regular" {
  block_device_mappings {
    device_name  = "/dev/xvdcz"
    virtual_name = "ephemeral0"
  }
  key_name = "gitlab"
  name     = "batch_instance_regular"
  tags = {
    "Name"            = "batch_instance_regular"
    "management:area" = "cost"
    "management:type" = "product"
  }
  user_data = filebase64("${path.module}/aws_batch_user_data")
}

locals {
  compute_environments_ec2 = {
    dedicated = {
      bid_percentage      = null
      instances           = 5
      spot_iam_fleet_role = null
      type                = "EC2"

      tags = {
        "Name"            = "dedicated"
        "management:area" = "cost"
        "management:type" = "product"
      }
      launch_template_id      = aws_launch_template.batch_instance_regular.id
      launch_template_version = aws_launch_template.batch_instance_regular.latest_version
    }
  }
  compute_environments_spot = {
    observes = {
      bid_percentage      = 100
      instances           = 3
      spot_iam_fleet_role = aws_iam_role.aws_ecs_instance_role.arn
      type                = "SPOT"

      tags = {
        "Name"            = "observes"
        "management:area" = "administrative"
        "management:type" = "other"
      }
      launch_template_id      = aws_launch_template.batch_instance_regular.id
      launch_template_version = aws_launch_template.batch_instance_regular.latest_version
    }
    spot = {
      bid_percentage      = 100
      instances           = 6
      spot_iam_fleet_role = aws_iam_role.aws_ecs_instance_role.arn
      type                = "SPOT"

      tags = {
        "Name"            = "spot"
        "management:area" = "cost"
        "management:type" = "product"
      }
      launch_template_id      = aws_launch_template.batch_instance_regular.id
      launch_template_version = aws_launch_template.batch_instance_regular.latest_version
    }
    skims_all = {
      bid_percentage = 100
      instances      = 1 * length(jsondecode(data.local_file.skims_queues.content))
      # the multiplier is the number of instances for each finding (legacy)
      spot_iam_fleet_role = aws_iam_role.aws_ecs_instance_role.arn
      type                = "SPOT"

      tags = {
        "Name"            = "skims_all"
        "management:area" = "cost"
        "management:type" = "product"
      }
      launch_template_id      = aws_launch_template.batch_instance_regular.id
      launch_template_version = aws_launch_template.batch_instance_regular.latest_version
    }
  }
  compute_environments_spot_skims = {
    for name, _ in jsondecode(data.local_file.skims_queues.content)
    : name => {
      bid_percentage      = 100
      instances           = 4
      spot_iam_fleet_role = aws_iam_role.aws_ecs_instance_role.arn
      type                = "SPOT"

      tags = {
        "Name"            = name
        "management:area" = "cost"
        "management:type" = "product"
      }
      launch_template_id      = aws_launch_template.batch_instance_regular.id
      launch_template_version = aws_launch_template.batch_instance_regular.latest_version
    }
  }
  compute_environments = merge(
    local.compute_environments_ec2,
    local.compute_environments_spot,
    local.compute_environments_spot_skims,
  )

  queues = [
    {
      name     = "soon"
      priority = 10
    },
    {
      name     = "later"
      priority = 1
    },
  ]

  compute_environment_names = [
    for name, _ in local.compute_environments : name
  ]
  instance_type = data.aws_ec2_instance_type.instance.instance_type
  instance_vcpus = (
    data.aws_ec2_instance_type.instance.default_cores
    * data.aws_ec2_instance_type.instance.default_threads_per_core
  )
}

resource "aws_batch_compute_environment" "default" {
  # https://forums.aws.amazon.com/thread.jspa?threadID=289427
  for_each = local.compute_environments

  compute_environment_name_prefix = "${each.key}_"
  depends_on                      = [aws_iam_role_policy_attachment.aws_batch_service_role]
  service_role                    = aws_iam_role.aws_batch_service_role.arn
  state                           = "ENABLED"
  type                            = "MANAGED"

  compute_resources {
    bid_percentage = each.value.bid_percentage
    image_id       = "ami-0c09d65d2051ada93"
    instance_role  = aws_iam_instance_profile.aws_ecs_instance_role.arn
    instance_type  = [local.instance_type]
    max_vcpus      = each.value.instances * local.instance_vcpus
    min_vcpus      = 0
    security_group_ids = [
      aws_security_group.aws_batch_compute_environment_security_group.id,
    ]
    spot_iam_fleet_role = each.value.spot_iam_fleet_role
    subnets = [
      aws_subnet.default.id,
    ]
    type = each.value.type
    tags = each.value.tags

    launch_template {
      launch_template_id = each.value.launch_template_id
      version            = each.value.launch_template_version
    }
  }
  lifecycle {
    create_before_destroy = true
  }
  tags = each.value.tags
}

resource "aws_batch_job_queue" "default" {
  for_each = {
    for data in setproduct(
      local.compute_environment_names,
      local.queues,
    ) :

    "${data[0]}_${data[1].name}" => {
      compute_environment = data[0]
      priority            = data[1].priority
      tags                = local.compute_environments[data[0]].tags
    }
  }
  compute_environments = [
    aws_batch_compute_environment.default[each.value.compute_environment].arn
  ]
  name     = each.key
  priority = each.value.priority
  state    = "ENABLED"
  tags     = each.value.tags
}


resource "aws_batch_job_definition" "default" {
  name = "default"
  tags = {
    "Name"            = "default"
    "management:area" = "cost"
    "management:type" = "product"
  }
  type = "container"

  # This can be overridden on a per-job basis so let's add default values
  container_properties = jsonencode({
    command = ["./build.sh", "--help"]
    image   = "registry.gitlab.com/fluidattacks/product/makes"
    memory  = 512
    vcpus   = 1
  })
}

resource "aws_batch_job_definition" "makes" {
  name = "makes"
  type = "container"
  container_properties = jsonencode({
    image = "ghcr.io/fluidattacks/makes:21.11"

    # Will be overridden on job submission
    memory = 1800
    vcpus  = 1

    mountPoints = [
      {
        sourceVolume  = "logs_skims"
        containerPath = "/var/logs/skims"
        readOnly      = false
      }
    ]
    volumes = [
      {
        name = "logs_skims"
        host = {
          sourcePath = "/var/log/skims/"
        }
      }
    ]
  })

  tags = {
    "Name"            = "makes"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_batch_job_definition" "skims_process_group" {
  name = "skims_process_group"
  type = "container"
  container_properties = jsonencode({
    image = "registry.gitlab.com/fluidattacks/product/skims-process-group:latest"

    # Will be overridden on job submission
    memory = 1800
    vcpus  = 1

    mountPoints = [
      {
        sourceVolume  = "service_data"
        containerPath = "/process_group/"
        readOnly      = false
      }
    ]
    volumes = [
      {
        name = "service_data"
        host = {
          sourcePath = "/process_group/"
        }
      }
    ]
  })

  tags = {
    "Name"            = "skims_process_group"
    "management:area" = "cost"
    "management:type" = "product"
  }
}
