# AWS

output "prod_secret_key_id_1" {
  sensitive = true
  value     = aws_iam_access_key.prod_1.id
}

output "prod_secret_key_1" {
  sensitive = true
  value     = aws_iam_access_key.prod_1.secret
}

output "prod_secret_key_id_2" {
  sensitive = true
  value     = aws_iam_access_key.prod_2.id
}

output "prod_secret_key_2" {
  sensitive = true
  value     = aws_iam_access_key.prod_2.secret
}

output "dev_secret_key_id_1" {
  sensitive = true
  value     = aws_iam_access_key.dev_1.id
}

output "dev_secret_key_1" {
  sensitive = true
  value     = aws_iam_access_key.dev_1.secret
}

output "dev_secret_key_id_2" {
  sensitive = true
  value     = aws_iam_access_key.dev_2.id
}

output "dev_secret_key_2" {
  sensitive = true
  value     = aws_iam_access_key.dev_2.secret
}


# CloudFlare

output "dev_api_token" {
  sensitive = true
  value     = cloudflare_api_token.dev.value
}

output "prod_api_token" {
  sensitive = true
  value     = cloudflare_api_token.prod.value
}
