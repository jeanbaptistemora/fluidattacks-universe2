resource "aws_kms_key" "a" {
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  description              = "KMS key 1"
  deletion_window_in_days  = 10
  enable_key_rotation      = true
}

resource "aws_kms_key" "a" {
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  description              = "KMS key 1"
  deletion_window_in_days  = 10
  enable_key_rotation      = false
}

resource "aws_kms_key" "a" {
  customer_master_key_spec = "RSA_2048"
  description              = "KMS key 1"
  deletion_window_in_days  = 10
  enable_key_rotation      = false
}

resource "aws_kms_key" "a" {
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  description              = "KMS key 1"
  deletion_window_in_days  = 10
}
