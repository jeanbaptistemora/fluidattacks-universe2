resource "aws_s3_bucket" "fi_analytics_bucket" {
  bucket = var.analytics_bucket_name

  tags = {
    "Name"               = "fluidintegrates.analytics"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "fi_analytics_bucket" {
  bucket = aws_s3_bucket.fi_analytics_bucket.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "fi_analytics_bucket" {
  bucket = aws_s3_bucket.fi_analytics_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "fi_analytics_bucket" {
  bucket = aws_s3_bucket.fi_analytics_bucket.id

  versioning_configuration {
    status     = "Enabled"
    mfa_delete = "Disabled"
  }
}
