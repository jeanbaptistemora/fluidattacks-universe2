output "integrates-dev-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.integrates-dev-key-1.id
}

output "integrates-dev-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.integrates-dev-key-1.secret
}

output "integrates-dev-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.integrates-dev-key-2.id
}

output "integrates-dev-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.integrates-dev-key-2.secret
}
