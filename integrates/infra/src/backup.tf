# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

locals {
  db_tables = [
    "fi_async_processing",
    "fi_authz",
    "fi_events",
    "FI_findings",
    "fi_portfolios",
    "FI_project_access",
    "fi_project_comments",
    "FI_projects",
    "FI_users",
    "FI_vulnerabilities",
    "integrates",
    "integrates_vms",
  ]
}

data "aws_iam_policy_document" "backup" {
  statement {
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type        = "Service"
      identifiers = ["backup.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "backup" {
  name               = "integrates-backup"
  assume_role_policy = data.aws_iam_policy_document.backup.json

  tags = {
    "Name"               = "integrates-backup"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
  }
}

resource "aws_iam_role_policy_attachment" "backup" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

resource "aws_iam_role_policy_attachment" "backup_restore" {
  role       = aws_iam_role.backup.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForRestores"
}

resource "aws_backup_vault" "main" {
  name        = "integrates-dynamodb-backup-vault"
  kms_key_arn = "arn:aws:kms:us-east-1:205810638802:key/d33073aa-19f8-4390-afa1-abcda2be27d7"

  tags = {
    "Name"               = "integrates-dynamodb-backup-vault"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
  }
}

resource "aws_backup_plan" "main" {
  name = "integrates-dynamodb-backup-plan"

  tags = {
    "Name"               = "integrates-dynamodb-backup-plan"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
  }

  rule {
    rule_name         = "integrates-dynamodb-backup-daily-rule"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 5 * * ? *)"
    lifecycle {
      delete_after = 7
    }
  }

  rule {
    rule_name         = "integrates-dynamodb-backup-weekly-rule"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(30 5 ? * SUN *)"
    lifecycle {
      delete_after = 84
    }
  }

  rule {
    rule_name         = "integrates-dynamodb-backup-monthly-rule"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 6 ? * 1#1 *)"
    lifecycle {
      delete_after = 1095
    }
  }

  rule {
    rule_name         = "integrates-dynamodb-backup-yearly-rule"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(30 6 ? JAN 1#1 *)"
    lifecycle {
      delete_after = 5475
    }
  }

}

resource "aws_backup_selection" "main" {
  iam_role_arn = aws_iam_role.backup.arn
  name         = "integrates_dynamodb_backup_selection"
  plan_id      = aws_backup_plan.main.id

  resources = [
    for table in local.db_tables : "arn:aws:dynamodb:us-east-1:205810638802:table/${table}"
  ]
}
