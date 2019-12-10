output "integrates-prod-secret-key-id" {
  sensitive = true
  value     = aws_iam_access_key.integrates-prod-key.id
}

output "integrates-prod-secret-key" {
  sensitive = true
  value     = aws_iam_access_key.integrates-prod-key.secret
}
