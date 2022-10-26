# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_s3_bucket" "machine_data" {
  bucket = "machine.data"

  tags = {
    "Name"               = "machine.data"
    "management:area"    = "cost"
    "management:product" = "machine"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

resource "aws_s3_bucket_acl" "machine_data" {
  bucket = aws_s3_bucket.machine_data.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "machine_data" {
  bucket = aws_s3_bucket.machine_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}


resource "aws_s3_bucket_lifecycle_configuration" "machine_data" {
  bucket = aws_s3_bucket.machine_data.id

  rule {
    id     = "machine_data_cache"
    status = "Enabled"

    filter {
      prefix = "cache/"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }

    expiration {
      days = 7
    }
  }
  rule {
    id     = "machine_data_configs"
    status = "Enabled"

    filter {
      prefix = "configs/"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }

    expiration {
      days = 7
    }
  }
  rule {
    id     = "machine_data_results"
    status = "Enabled"

    filter {
      prefix = "results/"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }

    expiration {
      days = 7
    }
  }
  rule {
    id     = "machine_celery_results_backend"
    status = "Enabled"

    filter {
      prefix = "celery_result_backend/"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }

    expiration {
      days = 7
    }
  }
}
