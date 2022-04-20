locals {
  compute_environments_ec2 = {
    dedicated = {
      bid_percentage      = null
      instances           = 5
      spot_iam_fleet_role = null
      type                = "EC2"

      tags = {
        "Name"               = "dedicated"
        "management:area"    = "cost"
        "management:product" = "common"
        "management:type"    = "product"
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
        "Name"               = "observes"
        "management:area"    = "administrative"
        "management:product" = "observes"
        "management:type"    = "other"
      }
      launch_template_id      = aws_launch_template.batch_instance_regular.id
      launch_template_version = aws_launch_template.batch_instance_regular.latest_version
    }
    reports = {
      bid_percentage      = 100
      instances           = 6
      spot_iam_fleet_role = aws_iam_role.aws_ecs_instance_role.arn
      type                = "SPOT"

      tags = {
        "Name"               = "reports"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
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
        "Name"               = "spot"
        "management:area"    = "cost"
        "management:product" = "common"
        "management:type"    = "product"
      }
      launch_template_id      = aws_launch_template.batch_instance_regular.id
      launch_template_version = aws_launch_template.batch_instance_regular.latest_version
    }
    skims_all = {
      bid_percentage = 100
      instances      = 4 * length(jsondecode(data.local_file.skims_queues.content))
      # the multiplier is the number of instances for each finding (legacy)
      spot_iam_fleet_role = aws_iam_role.aws_ecs_instance_role.arn
      type                = "SPOT"

      tags = {
        "Name"               = "skims_all"
        "management:area"    = "cost"
        "management:product" = "skims"
        "management:type"    = "product"
      }
      launch_template_id      = aws_launch_template.batch_instance_regular.id
      launch_template_version = aws_launch_template.batch_instance_regular.latest_version
    }
  }
  compute_environments = merge(
    local.compute_environments_ec2,
    local.compute_environments_spot,
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
  instance_types = {
    for name, _ in local.compute_environments :
    "${name}" => {
      instance_type = name == "skims_all" ? (
        [
          data.aws_ec2_instance_type.instance_large.instance_type,
          data.aws_ec2_instance_type.instance.instance_type
        ]
      ) : [data.aws_ec2_instance_type.instance.instance_type]
    }
  }
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
    instance_type  = local.instance_types["${each.key}"].instance_type
    max_vcpus      = each.value.instances * local.instance_vcpus
    min_vcpus      = 0
    security_group_ids = [
      aws_security_group.aws_batch_compute_environment_security_group.id,
    ]
    spot_iam_fleet_role = each.value.spot_iam_fleet_role
    subnets = [
      data.aws_subnet.batch_clone.id,
      data.aws_subnet.batch_main.id,
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
