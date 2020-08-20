output "asserts-prod-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.asserts-prod-key-1.id
}

output "asserts-prod-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.asserts-prod-key-1.secret
}

output "asserts-prod-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.asserts-prod-key-2.id
}

output "asserts-prod-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.asserts-prod-key-2.secret
}
