output "continuous-dev-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.continuous-dev-key-1.id
}

output "continuous-dev-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.continuous-dev-key-1.secret
}

output "continuous-dev-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.continuous-dev-key-2.id
}

output "continuous-dev-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.continuous-dev-key-2.secret
}
