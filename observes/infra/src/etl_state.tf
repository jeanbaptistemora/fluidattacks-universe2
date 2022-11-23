resource "aws_s3_bucket" "observes_state" {
  bucket = "observes.state"

  tags = {
    "Name"               = "observes.state"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

# Bucket logging
resource "aws_s3_bucket_logging" "observes_state_logs" {
  bucket = aws_s3_bucket.observes_state.id

  target_bucket = "common.logging"
  target_prefix = "log/observes.state"
}

resource "aws_s3_bucket_acl" "observes_state" {
  bucket = aws_s3_bucket.observes_state.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "observes_state" {
  bucket = aws_s3_bucket.observes_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "observes_state" {
  bucket = aws_s3_bucket.observes_state.id

  versioning_configuration {
    status     = "Enabled"
    mfa_delete = "Disabled"
  }
}
