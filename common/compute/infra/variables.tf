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

locals {
  schedules = {
    integrates_scheduler_clone_groups_roots = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.clone_groups_roots.main",
      ]

      schedule_expression = "cron(0 5,8,11,14,17,21 ? * 2-6 *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_clone_groups_roots"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_clone_groups_roots_vpn = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.clone_groups_roots_vpn.main",
      ]

      schedule_expression = "cron(30 6,11,16 ? * 2-6 *)"
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
    integrates_scheduler_delete_imamura_stakeholders = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.delete_imamura_stakeholders.main",
      ]

      schedule_expression = "cron(0 1 ? * * *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_delete_imamura_stakeholders"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_delete_obsolete_groups = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.delete_obsolete_groups.main",
      ]

      schedule_expression = "cron(0 2 ? * * *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_delete_obsolete_groups"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_delete_obsolete_orgs = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.delete_obsolete_orgs.main",
      ]

      schedule_expression = "cron(0 9 ? * * *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_delete_obsolete_orgs"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_event_report = {
      enabled = false
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
    integrates_scheduler_get_remediated_findings = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.get_remediated_findings.main",
      ]

      schedule_expression = "cron(30 5,16 ? * 2-6 *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_get_remediated_findings"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_machine_queue_all = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.machine_queue_all.main",
      ]

      schedule_expression = "cron(0 5 ? * 5 *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_machine_queue_all"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_machine_queue_re_attacks = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.machine_queue_re_attacks.main",
      ]

      schedule_expression = "cron(0 12,19 ? * 2-6 *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_machine_queue_re_attacks"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_refresh_toe_lines = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.refresh_toe_lines.main",
      ]

      schedule_expression = "cron(0 20 ? * 2-6 *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_refresh_toe_lines"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_reminder_notification = {
      enabled = false
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
    integrates_scheduler_report_squad_usage = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.report_squad_usage.main",
      ]

      schedule_expression = "cron(0 18,00 ? * * *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_report_squad_usage"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_requeue_actions = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.requeue_actions.main",
      ]

      schedule_expression = "cron(15 * ? * * *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_requeue_actions"
        "management:area"    = "cost"
        "management:product" = "integrates"
        "management:type"    = "product"
      }
    }
    integrates_scheduler_review_machine_executions = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.review_machine_executions.main",
      ]

      schedule_expression = "cron(30 * ? * 2-6 *)"
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
    integrates_scheduler_update_group_toe_vulns = {
      enabled = false
      command = [
        "m",
        "f",
        "/integrates/utils/scheduler",
        "prod",
        "schedulers.update_group_toe_vulns.main",
      ]

      schedule_expression = "cron(0 10 ? * * *)"
      queue               = "unlimited_spot"
      attempts            = 3
      timeout             = 86400
      cpu                 = 2
      memory              = 7200

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }

      tags = {
        "Name"               = "integrates_scheduler_update_group_toe_vulns"
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
