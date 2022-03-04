resource "aws_s3_bucket" "observes_migration" {
  acl    = "private"
  bucket = "observes.migration"
  tags = {
    "Name"               = "observes.migration"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  versioning {
    enabled    = false
    mfa_delete = false
  }
}
