output "web-dev-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.web-dev-key-1.id
}

output "web-dev-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.web-dev-key-1.secret
}

output "web-dev-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.web-dev-key-2.id
}

output "web-dev-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.web-dev-key-2.secret
}
