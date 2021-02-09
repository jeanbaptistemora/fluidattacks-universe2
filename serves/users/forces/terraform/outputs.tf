output "forces_prod_secret_key_id-1" {
  sensitive = true
  value     = aws_iam_access_key.forces_prod_key-1.id
}

output "forces_prod_secret_key-1" {
  sensitive = true
  value     = aws_iam_access_key.forces_prod_key-1.secret
}

output "forces_dev_secret_key_id-1" {
  sensitive = true
  value     = aws_iam_access_key.forces_dev_key-1.id
}

output "forces_dev_secret_key-1" {
  sensitive = true
  value     = aws_iam_access_key.forces_dev_key-1.secret
}
