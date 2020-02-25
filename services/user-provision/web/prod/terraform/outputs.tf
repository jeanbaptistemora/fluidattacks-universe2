output "web-prod-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.web-prod-key-1.id
}

output "web-prod-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.web-prod-key-1.secret
}

output "web-prod-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.web-prod-key-2.id
}

output "web-prod-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.web-prod-key-2.secret
}
