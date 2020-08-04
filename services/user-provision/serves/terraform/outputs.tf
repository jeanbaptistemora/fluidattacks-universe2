output "serves-dev-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.serves-dev-key-1.id
}

output "serves-dev-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.serves-dev-key-1.secret
}

output "serves-dev-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.serves-dev-key-2.id
}

output "serves-dev-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.serves-dev-key-2.secret
}

output "serves-prod-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.serves-prod-key-1.id
}

output "serves-prod-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.serves-prod-key-1.secret
}

output "serves-prod-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.serves-prod-key-2.id
}

output "serves-prod-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.serves-prod-key-2.secret
}
