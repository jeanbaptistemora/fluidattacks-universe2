output "dev-secret-key-id" {
  sensitive = true
  value     = aws_iam_access_key.melts-dev-key-1.id
}

output "dev-secret-key" {
  sensitive = true
  value     = aws_iam_access_key.melts-dev-key-1.secret
}

output "prod-secret-key-id" {
  sensitive = true
  value     = aws_iam_access_key.melts-prod-key-1.id
}

output "prod-secret-key" {
  sensitive = true
  value     = aws_iam_access_key.melts-prod-key-1.secret
}

