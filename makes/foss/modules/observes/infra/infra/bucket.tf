resource "aws_s3_bucket" "fluidanalytics" {
  bucket = "fluidanalytics"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    "Name"            = "docs.fluidattacks.com"
    "management:area" = "cost"
    "management:type" = "product"
  }

  versioning {
    enabled = true
  }
}
