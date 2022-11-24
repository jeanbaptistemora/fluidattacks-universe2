variable "branch" {}

locals {
  bucket   = "integrates.${var.branch}"
  endpoint = var.branch == "trunk" ? "https://app.fluidattacks.com" : "https://${var.branch}.app.fluidattacks.com"
  tags = {
    area = var.branch == "trunk" ? "cost" : "innovation"
  }
  versioning = var.branch == "trunk" ? "Enabled" : "Disabled"
}

resource "aws_s3_bucket" "main" {
  bucket = local.bucket

  tags = {
    "Name"               = local.bucket
    "management:area"    = local.tags.area
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "main" {
  bucket = aws_s3_bucket.main.id

  acl = "private"
}

resource "aws_s3_bucket_logging" "main" {
  bucket = aws_s3_bucket.main.id

  target_bucket = "common.logging"
  target_prefix = "log/${local.bucket}"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id

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

resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id

  versioning_configuration {
    status = local.versioning
  }
}

resource "aws_s3_bucket_cors_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["https://localhost:*", local.endpoint]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}
