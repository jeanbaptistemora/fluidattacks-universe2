output "dev-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.dev-key-1.id
}

output "dev-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.dev-key-1.secret
}

output "dev-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.dev-key-2.id
}

output "dev-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.dev-key-2.secret
}
