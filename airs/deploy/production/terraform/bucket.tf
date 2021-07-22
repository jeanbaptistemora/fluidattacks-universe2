# Common

data "aws_iam_policy_document" "main" {
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
      "${aws_s3_bucket.prod.arn}/*",
      "${aws_s3_bucket.dev.arn}/*",
    ]
    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}


# Production

resource "aws_s3_bucket" "prod" {
  bucket = "fluidattacks.com"
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
    error_document = "404/index.html"
  }

  tags = {
    "Name"               = "fluidattacks.com"
    "management:type"    = "production"
    "management:product" = "airs"
  }
}

resource "aws_s3_bucket_policy" "prod" {
  bucket = aws_s3_bucket.prod.id
  policy = data.aws_iam_policy_document.main.json
}


# Development

resource "aws_s3_bucket" "dev" {
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

resource "aws_s3_bucket_policy" "dev" {
  bucket = aws_s3_bucket.dev.id
  policy = data.aws_iam_policy_document.main.json
}
