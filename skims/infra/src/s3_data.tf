# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_s3_bucket" "skims_data" {
  bucket = "skims.data"

  tags = {
    "Name"               = "skims.data"
    "Management:Area"    = "cost"
    "Management:Product" = "skims"
    "Management:Type"    = "product"
    "Access"             = "private"
  }
}

resource "aws_s3_bucket_acl" "skims_data" {
  bucket = aws_s3_bucket.skims_data.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "skims_data" {
  bucket = aws_s3_bucket.skims_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "skims_data" {
  bucket = aws_s3_bucket.skims_data.id
  rule {
    id     = "skims_data_configs"
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
    id     = "skims_data_results"
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
    id     = "skims_celery_results_backend"
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

resource "aws_s3_bucket_versioning" "skims_data" {
  bucket = aws_s3_bucket.skims_data.id

  versioning_configuration {
    status     = "Enabled"
    mfa_delete = "Disabled"
  }
}

# Skims sca

resource "aws_s3_bucket" "skims_sca" {
  bucket = "skims.sca"

  tags = {
    "Name"               = "skims.sca"
    "Management:Area"    = "cost"
    "Management:Product" = "skims"
    "Management:Type"    = "product"
    "Access"             = "public-read"
  }
}

resource "aws_s3_bucket_versioning" "skims_sca" {
  bucket = aws_s3_bucket.skims_sca.id

  versioning_configuration {
    status     = "Enabled"
    mfa_delete = "Disabled"
  }
}

resource "aws_s3_bucket_acl" "skims_sca" {
  bucket = aws_s3_bucket.skims_sca.id

  acl = "public-read"
}

data "aws_iam_policy_document" "skims_sca" {
  statement {
    sid    = "AllowScaPublicRead"
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "${aws_s3_bucket.skims_sca.arn}/*",
    ]
  }
}

resource "aws_s3_bucket_policy" "skims_sca" {
  bucket = aws_s3_bucket.skims_sca.id
  policy = data.aws_iam_policy_document.skims_sca.json
}

resource "aws_s3_bucket_server_side_encryption_configuration" "skims_sca" {
  bucket = aws_s3_bucket.skims_sca.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_logging" "skims_sca" {
  bucket = aws_s3_bucket.skims_sca.id

  target_bucket = "common.logging"
  target_prefix = "log/skims_sca"
}
