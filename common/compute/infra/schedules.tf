variable "schedules" {}
variable "sizes" {}

locals {
  schedules = jsondecode(var.schedules)
  sizes     = jsondecode(var.sizes)
}

resource "aws_batch_job_definition" "schedule" {
  for_each = local.schedules

  name = each.key
  type = "container"

  container_properties = jsonencode(
    {
      image      = "ghcr.io/fluidattacks/makes:22.11"
      command    = each.value.command
      jobRoleArn = "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/${each.value.awsRole}"

      resourceRequirements = [
        {
          type  = "VCPU"
          value = tostring(local.sizes[each.value.size].cpu)
        },
        {
          type  = "MEMORY"
          value = tostring(local.sizes[each.value.size].memory)
        },
      ]

      environment = concat(
        each.value.environment,
        [
          {
            Name  = "CI"
            Value = "true"
          },
          {
            Name  = "MAKES_AWS_BATCH_COMPAT"
            Value = "true"
          },
        ]
      )
    }
  )

  retry_strategy {
    attempts = each.value.attempts
    evaluate_on_exit {
      action       = "RETRY"
      on_exit_code = 1
    }
    evaluate_on_exit {
      action    = "EXIT"
      on_reason = "CannotInspectContainerError:*"
    }
  }

  timeout {
    attempt_duration_seconds = each.value.timeout
  }

  tags           = each.value.tags
  propagate_tags = true
}


resource "aws_cloudwatch_event_rule" "main" {
  for_each = local.schedules

  name                = "schedule_${each.key}"
  is_enabled          = each.value.enable
  schedule_expression = each.value.scheduleExpression

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_target" "main" {
  for_each = local.schedules

  target_id = each.key
  rule      = aws_cloudwatch_event_rule.main[each.key].name
  arn       = aws_batch_job_queue.main[local.sizes[each.value.size].queue].arn
  role_arn  = data.aws_iam_role.main["prod_common"].arn

  batch_target {
    job_name       = each.key
    job_definition = aws_batch_job_definition.schedule[each.key].arn
    array_size     = each.value.parallel > 1 ? each.value.parallel : null
  }
}
