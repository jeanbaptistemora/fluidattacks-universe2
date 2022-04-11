# Production

resource "aws_s3_bucket" "bucket_prod" {
  bucket = "docs.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"

  tags = {
    "Name"               = "docs.fluidattacks.com"
    "management:area"    = "cost"
    "management:product" = "docs"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "prod" {
  bucket = aws_s3_bucket.bucket_prod.id

  acl = "private"
}

resource "aws_s3_bucket_website_configuration" "prod" {
  bucket = aws_s3_bucket.bucket_prod.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "404.html"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "prod" {
  bucket = aws_s3_bucket.bucket_prod.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

data "aws_iam_policy_document" "bucket_prod_policy" {
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
      "${aws_s3_bucket.bucket_prod.arn}/*",
    ]
    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "bucket_prod_policy" {
  bucket = aws_s3_bucket.bucket_prod.id
  policy = data.aws_iam_policy_document.bucket_prod_policy.json
}


# Development

resource "aws_s3_bucket" "bucket_dev" {
  bucket = "docs-dev.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"

  tags = {
    "Name"               = "docs-dev.fluidattacks.com"
    "management:area"    = "innovation"
    "management:product" = "docs"
    "management:type"    = "product"
  }
}

resource "aws_s3_bucket_acl" "dev" {
  bucket = aws_s3_bucket.bucket_dev.id

  acl = "private"
}

resource "aws_s3_bucket_website_configuration" "dev" {
  bucket = aws_s3_bucket.bucket_dev.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "404.html"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "dev" {
  bucket = aws_s3_bucket.bucket_dev.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

data "aws_iam_policy_document" "bucket_dev_policy" {
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
      "${aws_s3_bucket.bucket_dev.arn}/*",
    ]
    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "bucket_dev_policy" {
  bucket = aws_s3_bucket.bucket_dev.id
  policy = data.aws_iam_policy_document.bucket_dev_policy.json
}
