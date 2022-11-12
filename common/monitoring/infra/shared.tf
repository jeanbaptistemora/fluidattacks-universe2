# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
resource "aws_s3_bucket" "monitoring" {
  bucket = "common-monitoring"
}

resource "aws_s3_bucket" "monitoring_athena_results" {
  bucket = "common-monitoring-athena-results"
}

resource "aws_s3_bucket_lifecycle_configuration" "monitoring_athena_results" {
  bucket = aws_s3_bucket.monitoring_athena_results.id

  rule {
    id     = "remove old ${aws_s3_bucket.monitoring_athena_results.id} objects"
    status = "Enabled"

    expiration {
      days = 1
    }
  }
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.monitoring.id
  acl    = "private"
}

resource "aws_cloudwatch_log_group" "monitoring" {
  name = "common-monitoring"
}

resource "aws_athena_database" "monitoring" {
  name   = "common_monitoring"
  bucket = aws_s3_bucket.monitoring_athena_results.bucket
}

resource "aws_athena_workgroup" "monitoring" {
  name = "common-monitoring"

  configuration {
    result_configuration {
      output_location = "s3://${aws_s3_bucket.monitoring_athena_results.bucket}/"
    }
  }
}
