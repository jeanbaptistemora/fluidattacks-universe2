resource "aws_s3_bucket" "fi_analytics_bucket" {
  acl           = "private"
  bucket        = var.analytics_bucket_name
  region        = "us-east-1"
  request_payer = "BucketOwner"

  tags = {
    Pry                  = "Integrates"
    "management:type"    = "production"
    "management:product" = "integrates"
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
