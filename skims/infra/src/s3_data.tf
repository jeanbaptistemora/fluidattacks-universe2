resource "aws_s3_bucket" "skims_data" {
  bucket = "skims.data"

  tags = {
    "Name"               = "skims.data"
    "management:area"    = "cost"
    "management:product" = "skims"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "skims_data" {
  bucket = aws_s3_bucket.skims_data.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "skims_data" {
  bucket = aws_s3_bucket.skims_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "skims_data" {
  bucket = aws_s3_bucket.skims_data.id

  rule {
    id     = "skims_data_cache"
    status = "Enabled"

    filter {
      prefix = "cache/"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }

    expiration {
      days = 7
    }
  }
}

resource "aws_s3_bucket_versioning" "skims_data" {
  bucket = aws_s3_bucket.skims_data.id

  versioning_configuration {
    status     = "Enabled"
    mfa_delete = "Disabled"
  }
}
