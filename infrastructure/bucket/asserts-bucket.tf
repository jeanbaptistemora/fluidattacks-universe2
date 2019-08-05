variable "asserts-bucket" {}

resource "aws_s3_bucket" "asserts-bucket" {
  bucket = "${var.asserts-bucket}"
  acl    = "private"

  # Enable server-side encryption by default
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

