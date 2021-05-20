resource "aws_secretsmanager_secret" "forces_api_tokens" {
  for_each   = { for name in var.projects_forces : name => name }
  name       = "forces_token_${each.value}"
  kms_key_id = aws_kms_alias.keys_aliases[each.value].arn

  tags = {
    "Name"               = "integrates_api_token_forces"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}
