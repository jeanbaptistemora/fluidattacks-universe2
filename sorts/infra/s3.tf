resource "aws_s3_bucket" "sorts_bucket" {
  acl = "private"
  bucket = "sorts"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    "Name"               = "sorts"
    "management:type"    = "production"
    "management:product" = "sorts"
  }

  versioning {
    enabled = true
  }
}
