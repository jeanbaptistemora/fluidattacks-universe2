resource "aws_s3_bucket" "observes_state" {
  acl    = "private"
  bucket = "observes.state"
  tags = {
    "Name"            = "observes.state"
    "management:area" = "cost"
    "management:type" = "product"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  versioning {
    enabled    = true
    mfa_delete = false
  }
}
