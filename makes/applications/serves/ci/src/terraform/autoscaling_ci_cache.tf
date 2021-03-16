resource "aws_s3_bucket" "autoscaling_ci_cache" {
  bucket        = "autoscaling-ci-cache"
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
    "Name"               = "autoscaling-ci-cache"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}
