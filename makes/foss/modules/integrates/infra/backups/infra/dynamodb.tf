resource "aws_backup_vault" "integrates_dynamodb_backup_vault" {
  name        = "integrates-dynamodb-backup-vault"
  kms_key_arn = "arn:aws:kms:us-east-1:205810638802:key/d33073aa-19f8-4390-afa1-abcda2be27d7"

  tags = {
    "Name"            = "integrates-dynamodb-backup-vault"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_backup_plan" "integrates_dynamodb_backup_plan" {
  name = "integrates-dynamodb-backup-plan"

  tags = {
    "Name"            = "integrates-dynamodb-backup-plan"
    "management:area" = "cost"
    "management:type" = "product"
  }

  rule {
    rule_name         = "integrates-dynamodb-backup-daily-rule"
    target_vault_name = aws_backup_vault.integrates_dynamodb_backup_vault.name
    schedule          = "cron(0 5 * * ? *)"
    lifecycle {
      delete_after = 7
    }
  }

  rule {
    rule_name         = "integrates-dynamodb-backup-weekly-rule"
    target_vault_name = aws_backup_vault.integrates_dynamodb_backup_vault.name
    schedule          = "cron(30 5 ? * SUN *)"
    lifecycle {
      delete_after = 84
    }
  }

  rule {
    rule_name         = "integrates-dynamodb-backup-monthly-rule"
    target_vault_name = aws_backup_vault.integrates_dynamodb_backup_vault.name
    schedule          = "cron(0 6 ? * 1#1 *)"
    lifecycle {
      delete_after = 1095
    }
  }

  rule {
    rule_name         = "integrates-dynamodb-backup-yearly-rule"
    target_vault_name = aws_backup_vault.integrates_dynamodb_backup_vault.name
    schedule          = "cron(30 6 ? JAN 1#1 *)"
    lifecycle {
      delete_after = 5475
    }
  }

}

resource "aws_backup_selection" "dynamodb_backup_selection" {
  iam_role_arn = aws_iam_role.integrates-backup-role.arn
  name         = "integrates_dynamodb_backup_selection"
  plan_id      = aws_backup_plan.integrates_dynamodb_backup_plan.id

  resources = [
    for table in var.dynamodb-tables : "arn:aws:dynamodb:us-east-1:205810638802:table/${table}"
  ]
}
