output "sorts_prod_access_key-1" {
  sensitive = true
  value     = aws_iam_access_key.sorts_prod_key-1.id
}

output "sorts_prod_secret_key-1" {
  sensitive = true
  value     = aws_iam_access_key.sorts_prod_key-1.secret
}

output "sorts_prod_access_key-2" {
  sensitive = true
  value     = aws_iam_access_key.sorts_prod_key-2.id
}

output "sorts_prod_secret_key-2" {
  sensitive = true
  value     = aws_iam_access_key.sorts_prod_key-2.secret
}

output "sorts_dev_access_key-1" {
  sensitive = true
  value     = aws_iam_access_key.sorts_dev_key-1.id
}

output "sorts_dev_secret_key-1" {
  sensitive = true
  value     = aws_iam_access_key.sorts_dev_key-1.secret
}

output "sorts_dev_access_key-2" {
  sensitive = true
  value     = aws_iam_access_key.sorts_dev_key-2.id
}

output "sorts_dev_secret_key-2" {
  sensitive = true
  value     = aws_iam_access_key.sorts_dev_key-2.secret
}
