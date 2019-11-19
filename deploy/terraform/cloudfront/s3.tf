variable "bucket_name" {}
variable "evidences_bucket_name" {}

resource "aws_s3_bucket" "fi_resources_bucket" {
  bucket = var.bucket_name
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Pry = "Integrates"
  }
}

resource "aws_s3_bucket" "fi_evidences_bucket" {
  bucket = var.evidences_bucket_name
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Pry = "Integrates"
  }
}

data "aws_iam_policy_document" "cloudfront_s3_access" {
  statement {
    sid       = "CloudFrontAccess"
    effect    = "Allow"
    actions   = [
      "s3:GetObject"
    ]
    resources = [
      "${aws_s3_bucket.fi_evidences_bucket.arn}/*",
      "${aws_s3_bucket.fi_resources_bucket.arn}/*"
    ]

    principals {
      type        = "AWS"
      identifiers = [
        aws_cloudfront_origin_access_identity.cloudfront_identity.iam_arn
      ]
    }
  }
}

resource "aws_s3_bucket_policy" "fi_evidences_bucket_policy" {
  bucket = aws_s3_bucket.fi_evidences_bucket.id
  policy = data.aws_iam_policy_document.cloudfront_s3_access.json
}

resource "aws_s3_bucket_policy" "fi_resources_bucket_policy" {
  bucket = aws_s3_bucket.fi_resources_bucket.id
  policy = data.aws_iam_policy_document.cloudfront_s3_access.json
}

output "fi_evidences_bucket_id" {
  value = aws_s3_bucket.fi_evidences_bucket.id
}

output "fi_evidences_bucket_arn" {
  value = aws_s3_bucket.fi_evidences_bucket.arn
}

output "fi_resources_bucket_id" {
  value = aws_s3_bucket.fi_resources_bucket.id
}

output "fi_resources_bucket_arn" {
  value = aws_s3_bucket.fi_resources_bucket.arn
}
