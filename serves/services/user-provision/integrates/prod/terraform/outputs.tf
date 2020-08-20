output "integrates-prod-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.integrates-prod-key-1.id
}

output "integrates-prod-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.integrates-prod-key-1.secret
}

output "integrates-prod-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.integrates-prod-key-2.id
}

output "integrates-prod-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.integrates-prod-key-2.secret
}
