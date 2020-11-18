output "sorts_prod_access_key_1" {
  sensitive = true
  value     = aws_iam_access_key.sorts_prod_key_1.id
}

output "sorts_prod_secret_key_1" {
  sensitive = true
  value     = aws_iam_access_key.sorts_prod_key_1.secret
}

output "sorts_prod_access_key_2" {
  sensitive = true
  value     = aws_iam_access_key.sorts_prod_key_2.id
}

output "sorts_prod_secret_key_2" {
  sensitive = true
  value     = aws_iam_access_key.sorts_prod_key_2.secret
}

output "sorts_dev_access_key_1" {
  sensitive = true
  value     = aws_iam_access_key.sorts_dev_key_1.id
}

output "sorts_dev_secret_key_1" {
  sensitive = true
  value     = aws_iam_access_key.sorts_dev_key_1.secret
}

output "sorts_dev_access_key_2" {
  sensitive = true
  value     = aws_iam_access_key.sorts_dev_key_2.id
}

output "sorts_dev_secret_key_2" {
  sensitive = true
  value     = aws_iam_access_key.sorts_dev_key_2.secret
}
