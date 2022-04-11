resource "aws_s3_bucket" "fluidanalytics" {
  bucket = "fluidanalytics"

  tags = {
    "Name"               = "fluidanalytics"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "fluidanalytics" {
  bucket = aws_s3_bucket.fluidanalytics.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "fluidanalytics" {
  bucket = aws_s3_bucket.fluidanalytics.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "fluidanalytics" {
  bucket = aws_s3_bucket.fluidanalytics.id

  versioning_configuration {
    status     = "Enabled"
    mfa_delete = "Disabled"
  }
}
