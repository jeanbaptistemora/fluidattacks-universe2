output "skims_prod_secret_key_id_1" {
  sensitive = true
  value     = aws_iam_access_key.skims_prod_key_1.id
}

output "skims_prod_secret_key_1" {
  sensitive = true
  value     = aws_iam_access_key.skims_prod_key_1.secret
}
