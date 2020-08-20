output "okta-access-user-key" {
  sensitive = true
  value     = aws_iam_access_key.okta-access-user-key.secret
}
