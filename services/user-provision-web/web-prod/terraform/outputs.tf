output "web-prod-secret-key-id" {
  sensitive = true
  value     = aws_iam_access_key.web-prod-key.id
}

output "web-prod-secret-key" {
  sensitive = true
  value     = aws_iam_access_key.web-prod-key.secret
}
