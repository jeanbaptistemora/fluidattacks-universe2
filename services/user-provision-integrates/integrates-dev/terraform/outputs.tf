output "integrates-dev-secret-key-id" {
  sensitive = true
  value     = aws_iam_access_key.integrates-dev-key.id
}

output "integrates-dev-secret-key" {
  sensitive = true
  value     = aws_iam_access_key.integrates-dev-key.secret
}
