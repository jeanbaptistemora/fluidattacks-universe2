# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_s3_bucket" "common_logging" {
  bucket = "common.logging"

  tags = {
    "Name"               = "common.logging"
    "Management:Area"    = "innovation"
    "Management:Product" = "common"
    "Management:Type"    = "product"
    "Access"             = "private"
  }
}

resource "aws_s3_bucket_acl" "common_logging" {
  bucket = aws_s3_bucket.common_logging.id

  acl = "private"
}

resource "aws_s3_bucket_lifecycle_configuration" "common_logging" {
  bucket = aws_s3_bucket.common_logging.id

  rule {
    id     = "delete_logs"
    status = "Enabled"

    expiration {
      days = 180
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "common_logging" {
  bucket = aws_s3_bucket.common_logging.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
