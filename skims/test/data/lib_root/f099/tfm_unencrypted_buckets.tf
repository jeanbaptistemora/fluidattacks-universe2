resource "aws_s3_bucket" "unencrypted_bucket_1" {
  bucket = "my_unencrypted_bucket_1"
  acl    = "private"
  region = var.region
}

resource "aws_kms_key" "bucket_encryption_key" {
  description             = "This key is used to encrypt bucket objects"
  deletion_window_in_days = 10
}

resource "aws_s3_bucket" "encrypted_bucket_1" {
  bucket = "my_encrypted_bucket_1"
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = aws_kms_key.bucket_encryption_key.arn
        sse_algorithm     = "aws:kms"
      }
    }
  }
}

resource "aws_s3_bucket" "encrypted_bucket_2" {
  bucket = "my_encrypted_bucket_2"
  acl    = "private"
  region = var.region
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_2_encryption" {
  bucket = "my_encrypted_bucket_2"

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket" "encrypted_bucket_3" {
  bucket = "my_encrypted_bucket_3"
  acl    = "private"
  region = var.region
}

resource "aws_s3_bucket_server_side_encryption_configuration" "bucket_3_encryption" {
  bucket = aws_s3_bucket.encrypted_bucket_3.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
