resource "aws_s3_bucket" "ci_cache_buckets" {

  for_each = var.ci_cache_buckets

  bucket        = each.value
  acl           = "private"
  force_destroy = true

  versioning {
    enabled = false
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    "Name"               = each.value
    "management:type"    = "production"
    "management:product" = "makes"
  }
}
