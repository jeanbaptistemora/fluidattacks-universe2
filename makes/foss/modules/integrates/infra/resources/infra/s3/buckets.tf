resource "aws_s3_bucket" "fi_analytics_bucket" {
  acl           = "private"
  bucket        = var.analytics_bucket_name
  request_payer = "BucketOwner"

  tags = {
    "Name"               = "fluidintegrates.analytics"
    "management:area"    = "cost"
    "management:product" = "integrates"
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
    enabled    = true
    mfa_delete = false
  }
}
