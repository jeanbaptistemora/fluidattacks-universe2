resource "aws_s3_bucket" "sorts_bucket" {
  bucket = "sorts"

  tags = {
    "Name"               = "sorts"
    "management:area"    = "cost"
    "management:product" = "sorts"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "sorts_bucket" {
  bucket = aws_s3_bucket.sorts_bucket.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "sorts_bucket" {
  bucket = aws_s3_bucket.sorts_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "sorts_bucket" {
  bucket = aws_s3_bucket.sorts_bucket.id

  rule {
    id     = "training-job-configs"
    status = "Enabled"

    filter {
      prefix = "sorts-training-test"
    }

    expiration {
      days                         = 8
      expired_object_delete_marker = true
    }
  }
}

resource "aws_s3_bucket_versioning" "sorts_bucket" {
  bucket = aws_s3_bucket.sorts_bucket.id

  versioning_configuration {
    status     = "Enabled"
    mfa_delete = "Disabled"
  }
}
