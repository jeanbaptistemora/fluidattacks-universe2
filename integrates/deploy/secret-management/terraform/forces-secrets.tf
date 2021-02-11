resource "aws_secretsmanager_secret" "forces_api_tokens" {
  for_each   = { for name in var.projects_forces : name => name }
  name       = "forces_token_${each.value}"
  kms_key_id = "arn:aws:kms:us-east-1:${data.aws_caller_identity.current.account_id}:alias/forces_key_${each.value}"

  tags = {
    "Name"               = "integrates_api_token_forces"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}
