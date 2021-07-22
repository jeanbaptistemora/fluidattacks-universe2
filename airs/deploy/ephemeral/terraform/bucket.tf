resource "aws_s3_bucket" "web-ephemeral-bucket" {
  bucket = "web.eph.fluidattacks.com"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  website {
    index_document = "index.html"
    error_document = "error-index.html"
  }

  lifecycle_rule {
    id      = "remove_ephemerals"
    enabled = true

    expiration {
      days = 1
    }
  }

  tags = {
    "Name"               = "web.eph.fluidattacks.com"
    "management:type"    = "development"
    "management:product" = "airs"
  }
}

data "aws_iam_policy_document" "web-ephemeral-bucket-policy-data" {
  statement {
    sid    = "CloudFlare"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "${aws_s3_bucket.web-ephemeral-bucket.arn}/*",
    ]
    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "web-bucket-policy" {
  bucket = aws_s3_bucket.web-ephemeral-bucket.id
  policy = data.aws_iam_policy_document.web-ephemeral-bucket-policy-data.json
}
