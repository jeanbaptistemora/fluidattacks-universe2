resource "aws_backup_vault" "backup_vault" {
  name        = "integrates-backup-vault"
  kms_key_arn = "arn:aws:kms:us-east-1:205810638802:key/d33073aa-19f8-4390-afa1-abcda2be27d7"
}

resource "aws_backup_plan" "integrates_daily_backup_plan" {
  name = "integrates-daily-backup-plan"

  rule {
    rule_name         = "integrates-backup-daily-rule"
    target_vault_name = aws_backup_vault.backup_vault.name
    schedule          = "cron(0 5 * * ? *)"
    lifecycle {
      delete_after = 7
    }
  }
}

resource "aws_backup_plan" "integrates_weekly_backup_plan" {
  name = "integrates-weekly-backup-plan"

  rule {
    rule_name         = "integrates-backup-weekly-rule"
    target_vault_name = aws_backup_vault.backup_vault.name
    schedule          = "cron(0 6 * * 0 *)"
    lifecycle {
      delete_after = 84
    }
  }
}
