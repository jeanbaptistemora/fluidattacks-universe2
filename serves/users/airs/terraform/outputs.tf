# AWS

output "web-prod-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.web-prod-key-1.id
}

output "web-prod-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.web-prod-key-1.secret
}

output "web-prod-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.web-prod-key-2.id
}

output "web-prod-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.web-prod-key-2.secret
}

output "web-dev-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.web-dev-key-1.id
}

output "web-dev-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.web-dev-key-1.secret
}

output "web-dev-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.web-dev-key-2.id
}

output "web-dev-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.web-dev-key-2.secret
}


# CloudFlare

output "api_token_airs_development" {
  sensitive = true
  value     = cloudflare_api_token.airs_development.value
}

output "api_token_airs_production" {
  sensitive = true
  value     = cloudflare_api_token.airs_production.value
}
