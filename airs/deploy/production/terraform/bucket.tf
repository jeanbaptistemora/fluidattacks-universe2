resource "aws_s3_bucket" "bucket" {
  bucket = "fluidattacks.com"
  acl    = "private"
  region = var.region

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  website {
    index_document = "index.html"
    error_document = "error/index.html"
  }

  tags = {
    "Name"               = "fluidattacks.com"
    "management:type"    = "production"
    "management:product" = "airs"
  }
}
