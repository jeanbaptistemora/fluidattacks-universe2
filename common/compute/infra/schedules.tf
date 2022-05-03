# Schedule expressions:
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
# evaluateOnExit syntax:
# https://docs.aws.amazon.com/batch/latest/APIReference/API_EvaluateOnExit.html

locals {
  schedules = {
    common_criteria_test_unreferenced = {
      enabled = true
      command = ["m", "f", "/common/criteria/test/unreferenced"]

      schedule_expression = "cron(0/5 * * * ? *)"
      queue               = "unlimited_spot"
      attempts            = 1
      timeout             = 86400
      cpu                 = 0.5
      memory              = 1024

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "common_criteria_test_unreferenced"
        "management:area"    = "cost"
        "management:product" = "common"
        "management:type"    = "product"
      }
    }
  }
}

resource "aws_cloudwatch_event_rule" "main" {
  for_each = local.schedules

  name                = "schedule_${each.key}"
  is_enabled          = each.value.enabled
  schedule_expression = each.value.schedule_expression

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
  arn       = aws_batch_job_queue.main[each.value.queue].arn
  role_arn  = data.aws_iam_role.prod_common.arn

  input = jsonencode(
    {
      ContainerOverrides = {
        Command = each.value.command

        ResourceRequirements = [
          { Type = "VCPU", Value = each.value.cpu },
          { Type = "MEMORY", Value = each.value.memory },
        ]

        Environment = [
          for k, v in each.value.environment : { Name = k, Value = v }
        ]
      }

      Timeout = {
        AttemptDurationSeconds = each.value.timeout
      }
    }
  )

  batch_target {
    job_name       = each.key
    job_definition = aws_batch_job_definition.makes.arn
    job_attempts   = each.value.attempts
  }
}
