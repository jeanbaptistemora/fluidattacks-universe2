# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# Integrates main bucket

resource "aws_s3_bucket" "integrates" {
  bucket = "integrates"

  tags = {
    "Name"               = "integrates"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "integrates" {
  bucket = "integrates"

  acl = "private"
}

resource "aws_s3_bucket_logging" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  target_bucket = "common.logging"
  target_prefix = "log/integrates"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  rule {
    id     = "analytics"
    status = "Enabled"

    filter {
      prefix = "analytics/"
    }
    noncurrent_version_expiration {
      noncurrent_days = 14
    }
    expiration {
      days = 14
    }
  }
  rule {
    id     = "reports"
    status = "Enabled"

    filter {
      prefix = "reports/"
    }
    expiration {
      # 1 month + some timezone skews
      days = 32
    }
  }
}

resource "aws_s3_bucket_versioning" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_cors_configuration" "integrates" {
  bucket = aws_s3_bucket.integrates.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["https://app.fluidattacks.com", "https://localhost:*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}
