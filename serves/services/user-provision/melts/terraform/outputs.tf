output "dev-secret-key-id" {
  sensitive = true
  value     = aws_iam_access_key.dev-key.id
}

output "dev-secret-key" {
  sensitive = true
  value     = aws_iam_access_key.dev-key.secret
}

output "prod-secret-key-id" {
  sensitive = true
  value     = aws_iam_access_key.prod-key.id
}

output "prod-secret-key" {
  sensitive = true
  value     = aws_iam_access_key.prod-key.secret
}

