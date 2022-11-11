# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
resource "aws_s3_bucket" "monitoring" {
  bucket = "common-monitoring"
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.monitoring.id
  acl    = "private"
}

resource "aws_cloudwatch_log_group" "monitoring" {
  name = "common-monitoring"
}
