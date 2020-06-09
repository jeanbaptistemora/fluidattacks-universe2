variable "antivirus_bucket_name" {}

resource "aws_s3_bucket" "fi_antivirus_bucket" {
  bucket = var.antivirus_bucket_name
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Pry = "Integrates"
  }
}
