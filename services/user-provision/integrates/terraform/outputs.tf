output "integrates-dev-secret-key-id" {
  value = aws_iam_access_key.integrates-dev-key.id
}

output "integrates-dev-secret-key" {
  value = aws_iam_access_key.integrates-dev-key.secret
}
