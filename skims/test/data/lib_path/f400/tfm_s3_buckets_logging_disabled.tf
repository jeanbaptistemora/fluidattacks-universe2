resource "aws_s3_bucket" "state_bucket" {
  bucket        = "${data.aws_caller_identity.current.account_id}-terraform-state"
  acl           = var.acl
  force_destroy = var.force_destroy

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = aws_kms_key.mykey.arn
        sse_algorithm     = "aws:kms"
      }
    }
  }

}

resource "aws_s3_bucket" "logged_bucket" {
  bucket = "my_logged_bucket"
  acl    = "private"
}

resource "aws_s3_bucket" "log_bucket" {
  bucket = "my_log_bucket"
  acl    = "private"
}

resource "aws_s3_bucket_logging" "logging_config" {
  bucket        = aws_s3_bucket.logged_bucket.id
  target_bucket = aws_s3_bucket.log_bucket.id
}

resource "aws_s3_bucket" "non_logged_bucket" {
  bucket = "my_non_logged_bucket"
  acl    = "private"
}
