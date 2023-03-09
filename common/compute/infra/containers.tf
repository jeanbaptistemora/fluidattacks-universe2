resource "aws_batch_job_definition" "main" {
  for_each = data.aws_iam_role.main

  name = each.key
  type = "container"
  container_properties = jsonencode(
    {
      image      = "ghcr.io/fluidattacks/makes:latest"
      jobRoleArn = each.value.arn

      # Will be overridden on job submission
      resourceRequirements = [
        { type = "VCPU", value = "1" },
        { type = "MEMORY", value = "1900" },
      ]
    }
  )

  retry_strategy {
    attempts = 3
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
    attempt_duration_seconds = 86400
  }

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
