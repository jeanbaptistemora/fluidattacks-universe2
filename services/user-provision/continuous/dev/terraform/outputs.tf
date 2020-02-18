output "continuous-dev-secret-key-id" {
  sensitive = true
  value     = aws_iam_access_key.continuous-dev-key.id
}

output "continuous-dev-secret-key" {
  sensitive = true
  value     = aws_iam_access_key.continuous-dev-key.secret
}
