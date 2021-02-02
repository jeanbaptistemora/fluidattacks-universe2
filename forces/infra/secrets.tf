resource "aws_secretsmanager_secret" "forces_api_tokens" {
  for_each   = {for name in var.projects: name => name}
  name       = "forces-token-${each.value}"
  kms_key_id = "arn:aws:kms:us-east-1:205810638802:alias/continuous-${each.value}"

  tags = {
    "management:type"    = "production"
    "management:product" = "drills"
  }
}
