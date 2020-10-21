resource "aws_subnet" "default" {
  availability_zone = "${var.region}a"
  cidr_block = "192.168.8.0/23"
  map_public_ip_on_launch = true
  vpc_id = var.batch_vpc_id

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
  role = aws_iam_role.aws_ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
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
  role = aws_iam_role.aws_batch_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_security_group" "aws_batch_compute_environment_security_group" {
  name = "aws_batch_compute_environment_security_group"
  vpc_id = var.batch_vpc_id

  # AWS manage this things and it's unknown what source port, protocol or ip
  # will access the machine
  ingress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
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
      volume_size = 100
      volume_type = "gp2"
      delete_on_termination = true
    }
  }
}

resource "aws_batch_compute_environment" "default" {
  compute_environment_name = "default"
  depends_on = [aws_iam_role_policy_attachment.aws_batch_service_role]
  service_role = aws_iam_role.aws_batch_service_role.arn
  state = "ENABLED"
  type = "MANAGED"

  compute_resources {
    allocation_strategy = "SPOT_CAPACITY_OPTIMIZED"
    # We want to use this one: https://aws.amazon.com/amazon-linux-2
    #   because it provides Docker with overlay2,
    #   whose volumes are not limited to 10GB size but are elastic
    # This avoids us this problem:
    #   https://aws.amazon.com/premiumsupport/knowledge-center/increase-default-ecs-docker-limit/
    image_id = "ami-059628695ae4c249b"
    instance_role = aws_iam_instance_profile.aws_ecs_instance_role.arn
    instance_type = [
      "m5a.large",
      "m5a.xlarge",
    ]
    max_vcpus = 16
    min_vcpus = 0
    security_group_ids = [
      aws_security_group.aws_batch_compute_environment_security_group.id,
    ]
    subnets = [
      aws_subnet.default.id,
    ]
    type = "SPOT"
    tags = {
      "Name"               = "default"
      "management:type"    = "production"
      "management:product" = "common"
    }

    launch_template {
      // https://aws.amazon.com/premiumsupport/knowledge-center/batch-ebs-volumes-launch-template/
      launch_template_id = aws_launch_template.batch_instance.id
    }
  }
}

resource "aws_batch_compute_environment" "uninterruptible" {
  # Machines here do not use SPOT Instances in order to avoid jobs
  # being interrupted, this compute environment has a higher cost
  # (50% at the moment of writing) and will be used to run long-running
  # jobs that would otherwise be killed because of spot-machine interruption
  compute_environment_name = "uninterruptible"
  depends_on = [aws_iam_role_policy_attachment.aws_batch_service_role]
  service_role = aws_iam_role.aws_batch_service_role.arn
  state = "ENABLED"
  type = "MANAGED"

  compute_resources {
    allocation_strategy = "BEST_FIT_PROGRESSIVE"
    # We want to use this one: https://aws.amazon.com/amazon-linux-2
    #   because it provides Docker with overlay2,
    #   whose volumes are not limited to 10GB size but are elastic
    # This avoids us this problem:
    #   https://aws.amazon.com/premiumsupport/knowledge-center/increase-default-ecs-docker-limit/
    image_id = "ami-059628695ae4c249b"
    instance_role = aws_iam_instance_profile.aws_ecs_instance_role.arn
    instance_type = [
      "m5a.large",
      "m5a.xlarge",
    ]
    max_vcpus = 2
    min_vcpus = 0
    security_group_ids = [
      aws_security_group.aws_batch_compute_environment_security_group.id,
    ]
    subnets = [
      aws_subnet.default.id,
    ]
    # Higher cost, jobs can execute as much time as they need and won't
    # be interrupted unlike SPOT instances
    type = "EC2"
    tags = {
      "Name"               = "default"
      "management:type"    = "production"
      "management:product" = "common"
    }

    launch_template {
      // https://aws.amazon.com/premiumsupport/knowledge-center/batch-ebs-volumes-launch-template/
      launch_template_id = aws_launch_template.batch_instance.id
    }
  }
}

resource "aws_batch_job_queue" "default" {
  # Send here short-running jobs that can execute at any point in time
  # may be delayed by days
  compute_environments = [
    aws_batch_compute_environment.default.arn,
  ]
  name = "default"
  priority = 1
  state = "ENABLED"
}

resource "aws_batch_job_queue" "code_upload" {
  # Send here observes code_upload jobs
  compute_environments = [
    aws_batch_compute_environment.default.arn,
  ]
  name = "code_upload"
  priority = 2
  state = "ENABLED"
}

resource "aws_batch_job_queue" "mirror_s3" {
  # Send here observes mirror_s3 jobs
  compute_environments = [
    aws_batch_compute_environment.default.arn,
  ]
  name = "mirror_s3"
  priority = 3
  state = "ENABLED"
}

resource "aws_batch_job_queue" "asap" {
  # Send here short-running jobs that need to execute as soon as possible
  compute_environments = [
    aws_batch_compute_environment.default.arn,
  ]
  name = "asap"
  priority = 10
  state = "ENABLED"
}

resource "aws_batch_job_queue" "default-uninterruptible" {
  # Send here long-running jobs that can execute at any point in time
  # may be delayed by days
  # Just send here jobs that really need to run for many hours, it's more expensive
  compute_environments = [
    aws_batch_compute_environment.uninterruptible.arn,
  ]
  name = "default-uninterruptible"
  priority = 1
  state = "ENABLED"
}

resource "aws_batch_job_queue" "asap-uninterruptible" {
  # Send here long-running jobs that need to execute as soon as possible
  # Just send here jobs that really need to run for many hours, it's more expensive
  compute_environments = [
    aws_batch_compute_environment.uninterruptible.arn,
  ]
  name = "asap-uninterruptible"
  priority = 10
  state = "ENABLED"
}

resource "aws_batch_job_definition" "default" {
  name = "default"
  type = "container"

  # This can be overridden on a per-job basis so let's add default values
  container_properties = jsonencode({
    command = ["./build.sh", "--help"]
    image = "registry.gitlab.com/fluidattacks/product/bin:latest"
    memory = 512
    vcpus = 1
  })
}
