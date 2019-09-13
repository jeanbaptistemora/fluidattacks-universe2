variable "break-build-bucket" {}

resource "aws_s3_bucket" "break-build-bucket" {
  bucket = var.break-build-bucket
  region = var.region
  acl    = "private"
  versioning {
    enabled = true
  }

  # Enable server-side encryption by default
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

