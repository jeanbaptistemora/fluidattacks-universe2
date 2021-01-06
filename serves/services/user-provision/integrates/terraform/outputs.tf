# AWS

output "integrates-prod-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.integrates-prod-key-1.id
}

output "integrates-prod-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.integrates-prod-key-1.secret
}

output "integrates-prod-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.integrates-prod-key-2.id
}

output "integrates-prod-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.integrates-prod-key-2.secret
}

output "integrates-dev-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.integrates-dev-key-1.id
}

output "integrates-dev-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.integrates-dev-key-1.secret
}

output "integrates-dev-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.integrates-dev-key-2.id
}

output "integrates-dev-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.integrates-dev-key-2.secret
}


# CloudFlare

output "api_token_integrates_development" {
  sensitive = true
  value     = cloudflare_api_token.integrates_development.value
}

output "api_token_integrates_production" {
  sensitive = true
  value     = cloudflare_api_token.integrates_production.value
}
