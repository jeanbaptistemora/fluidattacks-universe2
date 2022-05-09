resource "aws_s3_bucket" "common_logging_bucket" {
  bucket = "common_logging"

  tags = {
    "Name"               = "common_logging"
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "common_logging_bucket" {
  bucket = aws_s3_bucket.common_logging_bucket.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "common_logging_bucket" {
  bucket = aws_s3_bucket.common_logging_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
