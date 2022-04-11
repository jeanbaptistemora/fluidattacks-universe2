# Production

resource "aws_s3_bucket" "prod" {
  bucket = "fluidattacks.com"

  tags = {
    "Name"               = "fluidattacks.com"
    "management:area"    = "cost"
    "management:product" = "airs"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "prod" {
  bucket = aws_s3_bucket.prod.id

  acl = "private"
}

resource "aws_s3_bucket_website_configuration" "prod" {
  bucket = aws_s3_bucket.prod.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "404/index.html"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "prod" {
  bucket = aws_s3_bucket.prod.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

data "aws_iam_policy_document" "bucket_prod" {
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
    ]
    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "prod" {
  bucket = aws_s3_bucket.prod.id
  policy = data.aws_iam_policy_document.bucket_prod.json
}


# Development

resource "aws_s3_bucket" "dev" {
  bucket = "web.eph.fluidattacks.com"

  tags = {
    "Name"               = "web.eph.fluidattacks.com"
    "management:area"    = "innovation"
    "management:product" = "airs"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "dev" {
  bucket = aws_s3_bucket.dev.id

  acl = "private"
}

resource "aws_s3_bucket_website_configuration" "dev" {
  bucket = aws_s3_bucket.dev.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error-index.html"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "dev" {
  bucket = aws_s3_bucket.dev.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "dev" {
  bucket = aws_s3_bucket.dev.id

  rule {
    id     = "remove_ephemerals"
    status = "Enabled"

    expiration {
      days = 1
    }
  }
}

data "aws_iam_policy_document" "bucket_dev" {
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
      "${aws_s3_bucket.dev.arn}/*",
    ]
    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "dev" {
  bucket = aws_s3_bucket.dev.id
  policy = data.aws_iam_policy_document.bucket_dev.json
}
