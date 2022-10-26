# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_s3_bucket" "etl_data" {
  bucket = "observes.etl-data"

  tags = {
    "Name"               = "observes.etl-data"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

resource "aws_s3_bucket_acl" "etl_data" {
  bucket = aws_s3_bucket.etl_data.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "etl_data" {
  bucket = aws_s3_bucket.etl_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
