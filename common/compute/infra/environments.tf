locals {
  environments = {
    small = {
      max_vcpus = 10000
      instances = ["c5ad.large"]
      subnets = [
        data.aws_subnet.batch_clone.id,
        data.aws_subnet.batch_main.id,
      ]
    }
    medium = {
      max_vcpus = 10000
      instances = ["c5ad.xlarge"]
      subnets = [
        data.aws_subnet.batch_clone.id,
        data.aws_subnet.batch_main.id,
      ]
    }
    large = {
      max_vcpus = 10000
      instances = ["c5ad.2xlarge"]
      subnets = [
        data.aws_subnet.batch_clone.id,
        data.aws_subnet.batch_main.id,
      ]
    }
    clone = {
      max_vcpus = 10000
      instances = ["c5ad.large"]
      subnets = [
        data.aws_subnet.batch_clone.id,
      ]
    }
  }
}

resource "aws_iam_instance_profile" "main" {
  name = "compute"
  role = data.aws_iam_role.prod_common.name
}

resource "aws_security_group" "main" {
  name   = "compute"
  vpc_id = data.aws_vpc.main.id

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
    "Name"               = "compute"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_launch_template" "main" {
  name     = "compute"
  key_name = "gitlab"

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      encrypted             = true
      delete_on_termination = true
      volume_size           = 15
      volume_type           = "gp3"
    }
  }

  block_device_mappings {
    device_name  = "/dev/xvdcz"
    virtual_name = "ephemeral0"
  }

  tag_specifications {
    resource_type = "volume"

    tags = {
      "Name"               = "compute"
      "management:area"    = "cost"
      "management:product" = "common"
      "management:type"    = "product"
    }
  }

  tags = {
    "Name"               = "compute"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }

  user_data = filebase64("${path.module}/aws_batch_user_data")
}

resource "aws_batch_compute_environment" "main" {
  for_each = local.environments

  compute_environment_name_prefix = "${each.key}_"

  service_role = data.aws_iam_role.prod_common.arn
  state        = "ENABLED"
  type         = "MANAGED"

  compute_resources {
    bid_percentage = 100
    image_id       = "ami-0c09d65d2051ada93"
    type           = "SPOT"

    max_vcpus = each.value.max_vcpus
    min_vcpus = 0

    instance_role       = aws_iam_instance_profile.main.arn
    spot_iam_fleet_role = data.aws_iam_role.prod_common.arn

    instance_type      = each.value.instances
    security_group_ids = [aws_security_group.main.id]
    subnets            = each.value.subnets

    tags = {
      "Name"               = each.key
      "management:area"    = "cost"
      "management:product" = "common"
      "management:type"    = "product"
    }

    launch_template {
      launch_template_id = aws_launch_template.main.id
      version            = aws_launch_template.main.latest_version
    }
  }

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_batch_job_queue" "main" {
  for_each = local.environments

  name                 = each.key
  state                = "ENABLED"
  priority             = 1
  compute_environments = [aws_batch_compute_environment.main[each.key].arn]

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
