output "dev-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.melts-dev-key-1.id
}

output "dev-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.melts-dev-key-1.secret
}

output "dev-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.melts-dev-key-2.id
}

output "dev-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.melts-dev-key-2.secret
}

output "prod-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.melts-prod-key-1.id
}

output "prod-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.melts-prod-key-1.secret
}

output "prod-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.melts-prod-key-2.id
}

output "prod-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.melts-prod-key-2.secret
}

