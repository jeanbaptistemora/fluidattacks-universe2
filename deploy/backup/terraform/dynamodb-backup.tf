resource "aws_backup_plan" "dynamodb_backup_plan" {
  name = "dynamodb_backup_plan"

  rule {
    rule_name         = "dynamodb_backup_rule"
    target_vault_name = "aws_backup_vault.dynamodb_backup_vault.name"
    schedule          = "cron(0 12 * * ? *)"
  }
}

resource "aws_backup_vault" "dynamodb_backup_vault" {
  name        = "dynamodb_backup_vault"
  kms_key_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/integrates-prod-policy"
}
