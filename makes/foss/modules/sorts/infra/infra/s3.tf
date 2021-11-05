resource "aws_s3_bucket" "sorts_bucket" {
  acl    = "private"
  bucket = "sorts"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  lifecycle_rule {
    id      = "training-job-configs"
    prefix  = "sorts-training-test"
    enabled = true

    expiration {
      days                         = 8
      expired_object_delete_marker = true
    }
  }

  tags = {
    "Name"            = "sorts"
    "management:area" = "cost"
    "management:type" = "product"
  }

  versioning {
    enabled = true
  }
}
