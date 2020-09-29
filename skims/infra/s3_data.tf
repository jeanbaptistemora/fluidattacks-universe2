resource "aws_s3_bucket" "skims_data" {
  acl = "private"
  bucket = "skims.data"
  region = var.region
  tags = {
    Product = "Skims"
    "management:type"    = "production"
    "management:product" = "skims"
  }

  lifecycle_rule {
    abort_incomplete_multipart_upload_days = 7
    enabled = true
    id = "skims_data_cache"
    prefix = "cache/"

    expiration {
      days = 28
    }

    noncurrent_version_expiration {
      days = 28
    }
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  versioning {
    enabled = true
    mfa_delete = false
  }
}
