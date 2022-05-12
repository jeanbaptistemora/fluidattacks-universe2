resource "aws_s3_bucket" "state_bucket" {
  bucket        = "${data.aws_caller_identity.current.account_id}-terraform-state"
  acl           = var.acl
  force_destroy = var.force_destroy

  versioning {
    enabled = false
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

resource "aws_s3_bucket" "versioned_bucket_1" {
  bucket = "my_versioned_bucket_1"
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "versioning_config_1" {
  bucket = aws_s3_bucket.versioned_bucket_1.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "non_versioned_bucket_1" {
  bucket = "my_non_versioned_bucket_1"
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "versioning_config_2" {
  bucket = "my_non_versioned_bucket_1"
  versioning_configuration {
    status = "Suspended"
  }
}
