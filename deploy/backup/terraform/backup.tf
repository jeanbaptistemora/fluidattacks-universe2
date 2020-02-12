resource "aws_backup_vault" "backup_vault" {
  name        = "integrates-backup-vault"
  kms_key_arn = "arn:aws:kms:us-east-1:205810638802:key/d33073aa-19f8-4390-afa1-abcda2be27d7"
}

resource "aws_backup_plan" "integrates_backup_plan" {
  name = "integrates-backup-plan"

  rule {
    rule_name         = "integrates-backup-rule"
    target_vault_name = aws_backup_vault.backup_vault.name
    schedule          = "cron(0 0 * * ? *)"
  }
}
