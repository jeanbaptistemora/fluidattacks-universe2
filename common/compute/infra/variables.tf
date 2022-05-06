data "aws_caller_identity" "current" {}
variable "region" {
  default = "us-east-1"
}
variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}

# Schedules

variable "productApiToken" {
  sensitive = true
}

# Schedule expressions:
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
# evaluateOnExit syntax:
# https://docs.aws.amazon.com/batch/latest/APIReference/API_EvaluateOnExit.html

locals {
  schedules = {
    integrates_scheduler_clone_groups_roots_vpn = {
      enabled = true
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.clone_groups_roots_vpn.main",
      ]

      schedule_expression = "cron(30 6,11,16 ? * 1-5 *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_clone_groups_roots_vpn"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_event_report = {
      enabled = true
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.event_report.main",
      ]

      schedule_expression = "cron(0 14 ? * * *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_event_report"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_reminder_notification = {
      enabled = true
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.reminder_notification.main",
      ]

      schedule_expression = "cron(0 19 ? * * *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_reminder_notification"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_review_machine_executions = {
      enabled = true
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.review_machine_executions.main",
      ]

      schedule_expression = "cron(30 * ? * 1-5 *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_review_machine_executions"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
  }
}

# Reused infrastructure

data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "batch_clone" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["batch_clone"]
  }
}
data "aws_subnet" "batch_main" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["batch_main"]
  }
}
data "aws_iam_role" "prod_common" {
  name = "prod_common"
}
