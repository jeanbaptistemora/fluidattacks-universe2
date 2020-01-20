output "continuous-prod-secret-key-id" {
  sensitive = true
  value     = aws_iam_access_key.continuous-prod-key.id
}

output "continuous-prod-secret-key" {
  sensitive = true
  value     = aws_iam_access_key.continuous-prod-key.secret
}
