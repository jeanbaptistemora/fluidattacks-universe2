resource "aws_subnet" "default" {
  availability_zone       = "${var.region}a"
  cidr_block              = "192.168.8.0/23"
  map_public_ip_on_launch = true
  vpc_id                  = var.batch_vpc_id

  tags = {
    "Name"               = "batch"
    "management:type"    = "production"
    "management:product" = "common"
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
    "Name"               = "aws_ecs_instance_role"
    "management:type"    = "production"
    "management:product" = "common"
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
    "Name"               = "aws_batch_service_role"
    "management:type"    = "production"
    "management:product" = "common"
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
    "Name"               = "aws_batch_compute_environment_security_group"
    "management:type"    = "production"
    "management:product" = "common"
  }
}

resource "aws_launch_template" "batch_instance" {
  name = "batch_instance"
  tags = {
    "Name"               = "batch_instance"
    "management:type"    = "production"
    "management:product" = "common"
  }
  user_data = filebase64("${path.module}/aws_batch_user_data")

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      volume_size           = 100
      volume_type           = "gp3"
      delete_on_termination = true
    }
  }
}

locals {
  # Most of the parameters cant be updated in-place
  # So just comment items, apply (to destroy the item)
  # then un-comment, modify, and apply (to create the item again from scratch)
  compute_environments = {
    skims = {
      bid_percentage      = 100
      max_vcpus           = 32
      spot_iam_fleet_role = aws_iam_role.aws_ecs_instance_role.arn
      type                = "SPOT"
    },
    spot = {
      bid_percentage      = 100
      max_vcpus           = 16
      spot_iam_fleet_role = aws_iam_role.aws_ecs_instance_role.arn
      type                = "SPOT"
    },
    dedicated = {
      bid_percentage      = null
      max_vcpus           = 4
      spot_iam_fleet_role = null
      type                = "EC2"
    },
  }
  queues = [
    {
      name     = "now"
      priority = 10
    },
    {
      name     = "soon"
      priority = 5
    },
    {
      name     = "later"
      priority = 1
    },
  ]

  compute_environment_names = [
    for name, _ in local.compute_environments : name
  ]
}

resource "aws_batch_compute_environment" "default" {
  for_each = local.compute_environments

  compute_environment_name = each.key
  depends_on               = [aws_iam_role_policy_attachment.aws_batch_service_role]
  service_role             = aws_iam_role.aws_batch_service_role.arn
  state                    = "ENABLED"
  type                     = "MANAGED"

  compute_resources {
    bid_percentage = each.value.bid_percentage
    # We want to use this one: https://aws.amazon.com/amazon-linux-2
    #   because it provides Docker with overlay2,
    #   whose volumes are not limited to 10GB size but are elastic
    # This avoids us this problem:
    #   https://aws.amazon.com/premiumsupport/knowledge-center/increase-default-ecs-docker-limit/
    image_id      = "ami-059628695ae4c249b"
    instance_role = aws_iam_instance_profile.aws_ecs_instance_role.arn
    instance_type = [
      "m5a.xlarge",
    ]
    max_vcpus = each.value.max_vcpus
    min_vcpus = 0
    security_group_ids = [
      aws_security_group.aws_batch_compute_environment_security_group.id,
    ]
    spot_iam_fleet_role = each.value.spot_iam_fleet_role
    subnets = [
      aws_subnet.default.id,
    ]
    type = each.value.type
    tags = {
      "Name"               = each.key
      "management:type"    = "production"
      "management:product" = "common"
    }

    launch_template {
      // https://aws.amazon.com/premiumsupport/knowledge-center/batch-ebs-volumes-launch-template/
      launch_template_id = aws_launch_template.batch_instance.id
    }
  }

  tags = {
    "Name"               = "default"
    "management:type"    = "production"
    "management:product" = "common"
  }
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
    }
  }
  compute_environments = [
    aws_batch_compute_environment.default[each.value.compute_environment].arn
  ]
  name     = each.key
  priority = each.value.priority
  state    = "ENABLED"
  tags = {
    "Name"               = "default"
    "management:type"    = "production"
    "management:product" = "common"
  }
}

resource "aws_batch_job_definition" "default" {
  name = "default"
  tags = {
    "Name"               = "default"
    "management:type"    = "production"
    "management:product" = "common"
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
