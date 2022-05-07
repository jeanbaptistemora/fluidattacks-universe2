resource "aws_s3_bucket" "common_logging_bucket" {
  bucket = "common_logging"
  acl    = "private"

  tags = {
    "Name"               = "common_logging"
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

}
