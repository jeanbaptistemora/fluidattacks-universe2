resource "aws_backup_plan" "integrates_backup_plan" {
  name = "integrates-backup-plan"

  rule {
    rule_name         = "integrates-backup-daily-rule"
    target_vault_name = aws_backup_vault.backup_vault.name
    schedule          = "cron(0 5 * * ? *)"
    lifecycle {
      delete_after = 7
    }
  }

  rule {
    rule_name         = "integrates-backup-weekly-rule"
    target_vault_name = aws_backup_vault.backup_vault.name
    schedule          = "cron(30 5 ? * SUN *)"
    lifecycle {
      delete_after = 84
    }
  }

  rule {
    rule_name         = "integrates-backup-monthly-rule"
    target_vault_name = aws_backup_vault.backup_vault.name
    schedule          = "cron(0 6 ? * 1#1 *)"
    lifecycle {
      delete_after = 1095
    }
  }

  rule {
    rule_name         = "integrates-backup-yearly-rule"
    target_vault_name = aws_backup_vault.backup_vault.name
    schedule          = "cron(30 6 ? JAN 1#1 *)"
    lifecycle {
      delete_after = 5475
    }
  }

}

resource "aws_backup_selection" "dynamodb_backup_selection" {
  iam_role_arn = aws_iam_role.integrates-backup-role.arn
  name         = "integrates_dynamodb_backup_selection"
  plan_id      = aws_backup_plan.integrates_backup_plan.id

  resources    = [
    for table in var.dynamodb-tables : "arn:aws:dynamodb:us-east-1:205810638802:table/${table}"
  ]
}
