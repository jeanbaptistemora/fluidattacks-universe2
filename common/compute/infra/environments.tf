locals {
  machine_sizes = {
    small = {
      max_vcpus = 10000
      instances = ["c5ad.large"]
    }
    medium = {
      max_vcpus = 10000
      instances = ["c5ad.xlarge"]
    }
    large = {
      max_vcpus = 10000
      instances = ["c5ad.2xlarge"]
    }
  }
  config = {
    common = {
      product = "common"
      subnets = [
        data.aws_subnet.batch_clone.id,
        data.aws_subnet.batch_main.id,
      ]
      type = "SPOT"
    }
    forces = {
      product = "forces"
      subnets = [
        data.aws_subnet.batch_clone.id,
        data.aws_subnet.batch_main.id,
      ]
      type = "SPOT"
    }
    integrates = {
      product = "integrates"
      subnets = [
        data.aws_subnet.batch_clone.id,
        data.aws_subnet.batch_main.id,
      ]
      type = "SPOT"
    }
    skims = {
      product = "skims"
      subnets = [
        data.aws_subnet.batch_clone.id,
        data.aws_subnet.batch_main.id,
      ]
      type = "SPOT"
    }
    sorts = {
      product = "sorts"
      subnets = [
        data.aws_subnet.batch_clone.id,
        data.aws_subnet.batch_main.id,
      ]
      type = "SPOT"
    }
    observes = {
      product = "observes"
      subnets = [
        data.aws_subnet.batch_main.id,
      ]
      type = "SPOT"
    }

  }
  environments = {
    small = merge(
      local.machine_sizes.small,
      local.config.common
    )
    medium = merge(
      local.machine_sizes.medium,
      local.config.common
    )
    large = merge(
      local.machine_sizes.large,
      local.config.common
    )
    clone = merge(
      local.machine_sizes.small,
      local.config.common,
      {
        subnets = [
          data.aws_subnet.batch_clone.id,
        ]
      }
    )
    common_small = merge(
      local.machine_sizes.small,
      local.config.common
    )
    forces_small = merge(
      local.machine_sizes.small,
      local.config.forces
    )
    integrates_small = merge(
      local.machine_sizes.small,
      local.config.integrates
    )
    integrates_medium = merge(
      local.machine_sizes.medium,
      local.config.integrates
    )
    integrates_large = merge(
      local.machine_sizes.large,
      local.config.integrates,
    )
    observes_clone = merge(
      local.machine_sizes.small,
      local.config.observes,
      {
        subnets = [
          data.aws_subnet.batch_clone.id,
        ]
      }
    )
    observes_small = merge(
      local.machine_sizes.small,
      local.config.observes
    )
    observes_medium = merge(
      local.machine_sizes.medium,
      local.config.observes
    )
    observes_large = merge(
      local.machine_sizes.large,
      local.config.observes,
    )
    skims_small = merge(
      local.machine_sizes.small,
      local.config.skims
    )
    skims_medium = merge(
      local.machine_sizes.medium,
      local.config.skims
    )
    skims_large = merge(
      local.machine_sizes.large,
      local.config.skims,
    )
    sorts_small = merge(
      local.machine_sizes.small,
      local.config.sorts
    )
    sorts_large = merge(
      local.machine_sizes.large,
      local.config.sorts,
    )
  }
}

resource "aws_security_group" "main" {
  name   = "compute"
  vpc_id = data.aws_vpc.main.id

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
  name                                 = "compute"
  key_name                             = "gitlab"
  instance_initiated_shutdown_behavior = "terminate"

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

  user_data               = filebase64("${path.module}/aws_batch_user_data")
  disable_api_termination = true
  vpc_security_group_ids  = [aws_security_group.main.id]
}

resource "aws_batch_compute_environment" "main" {
  for_each = local.environments

  compute_environment_name_prefix = "${each.key}_"

  service_role = data.aws_iam_role.main["prod_common"].arn
  state        = "ENABLED"
  type         = "MANAGED"

  compute_resources {
    bid_percentage = 100
    image_id       = "ami-0c09d65d2051ada93"
    type           = each.value.type

    max_vcpus = each.value.max_vcpus
    min_vcpus = 0

    instance_role       = data.aws_iam_instance_profile.main["ecsInstanceRole"].arn
    spot_iam_fleet_role = data.aws_iam_role.main["prod_common"].arn

    instance_type      = each.value.instances
    security_group_ids = [aws_security_group.main.id]
    subnets            = each.value.subnets

    tags = {
      "Name"               = each.key
      "management:area"    = "cost"
      "management:product" = each.value.product
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
    "management:product" = each.value.product
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
    "management:product" = each.value.product
    "management:type"    = "product"
  }
}
