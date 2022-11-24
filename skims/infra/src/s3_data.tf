# Skims sca

resource "aws_s3_bucket" "skims_sca" {
  bucket = "skims.sca"

  tags = {
    "Name"               = "skims.sca"
    "management:area"    = "cost"
    "management:product" = "skims"
    "management:type"    = "product"
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
