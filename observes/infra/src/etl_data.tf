resource "aws_s3_bucket" "etl_data" {
  bucket = "observes.etl-data"

  tags = {
    "Name"               = "observes.etl-data"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

# Bucket logging
resource "aws_s3_bucket_logging" "etl_data_logs" {
  bucket = aws_s3_bucket.etl_data.id

  target_bucket = "common.logging"
  target_prefix = "log/observes.etl-data"
}

#Bucket versioning
resource "aws_s3_bucket_versioning" "etl_data_versioning" {
  bucket = aws_s3_bucket.etl_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_acl" "etl_data" {
  bucket = aws_s3_bucket.etl_data.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "etl_data" {
  bucket = aws_s3_bucket.etl_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
