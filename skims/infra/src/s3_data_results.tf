resource "aws_s3_bucket" "skims_results" {
  bucket = "skims.results"

  tags = {
    "Name"               = "skims.results"
    "management:area"    = "cost"
    "management:product" = "skims"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "skims_results" {
  bucket = aws_s3_bucket.skims_results.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "skims_results" {
  bucket = aws_s3_bucket.skims_results.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "skims_results" {
  bucket = aws_s3_bucket.skims_results.id

  rule {
    id     = "skims_results"
    status = "Enabled"

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

resource "aws_s3_bucket_versioning" "skims_results" {
  bucket = aws_s3_bucket.skims_results.id

  versioning_configuration {
    status     = "Suspended"
    mfa_delete = "Disabled"
  }
}
