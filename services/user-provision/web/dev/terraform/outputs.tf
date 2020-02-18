output "web-dev-secret-key-id" {
  sensitive = true
  value     = aws_iam_access_key.web-dev-key.id
}

output "web-dev-secret-key" {
  sensitive = true
  value     = aws_iam_access_key.web-dev-key.secret
}
