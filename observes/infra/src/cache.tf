# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_s3_bucket" "observes_cache" {
  bucket = "observes.cache"

  tags = {
    "Name"               = "observes.cache"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

resource "aws_s3_bucket_acl" "observes_cache" {
  bucket = aws_s3_bucket.observes_cache.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "observes_cache" {
  bucket = aws_s3_bucket.observes_cache.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
