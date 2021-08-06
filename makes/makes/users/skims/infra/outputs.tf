output "skims_prod_secret_key_id-1" {
  sensitive = true
  value     = aws_iam_access_key.skims_prod_key-1.id
}

output "skims_prod_secret_key-1" {
  sensitive = true
  value     = aws_iam_access_key.skims_prod_key-1.secret
}

output "skims_prod_secret_key_id-2" {
  sensitive = true
  value     = aws_iam_access_key.skims_prod_key-2.id
}

output "skims_prod_secret_key-2" {
  sensitive = true
  value     = aws_iam_access_key.skims_prod_key-2.secret
}

output "skims_dev_secret_key_id-1" {
  sensitive = true
  value     = aws_iam_access_key.skims_dev_key-1.id
}

output "skims_dev_secret_key-1" {
  sensitive = true
  value     = aws_iam_access_key.skims_dev_key-1.secret
}

output "skims_dev_secret_key_id-2" {
  sensitive = true
  value     = aws_iam_access_key.skims_dev_key-2.id
}

output "skims_dev_secret_key-2" {
  sensitive = true
  value     = aws_iam_access_key.skims_dev_key-2.secret
}
