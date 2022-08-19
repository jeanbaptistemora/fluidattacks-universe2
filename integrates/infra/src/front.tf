# Development

resource "aws_s3_bucket" "dev" {
  bucket = "integrates.front.development.fluidattacks.com"

  tags = {
    "Name"               = "integrates.front.development.fluidattacks.com"
    "management:area"    = "innovation"
    "management:product" = "integrates"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

resource "aws_s3_bucket_acl" "dev" {
  bucket = aws_s3_bucket.dev.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "dev" {
  bucket = aws_s3_bucket.dev.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_cors_configuration" "dev" {
  bucket = aws_s3_bucket.dev.id

  cors_rule {
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = [
      "https://app.fluidattacks.com",
      "https://integrates.front.development.fluidattacks.com"
    ]
    max_age_seconds = 3000
  }
}

data "aws_iam_policy_document" "dev" {
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
  policy = data.aws_iam_policy_document.dev.json
}

resource "cloudflare_page_rule" "dev" {
  zone_id  = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  target   = "integrates.front.development.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  status   = "active"
  priority = 1

  actions {
    cache_level       = "aggressive"
    edge_cache_ttl    = 1800
    browser_cache_ttl = 1800
  }
}

resource "cloudflare_record" "dev" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "integrates.front.development.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.dev.bucket_domain_name
  proxied = true
  ttl     = 1
}

# Production

resource "aws_s3_bucket" "prod" {
  bucket = "integrates.front.production.fluidattacks.com"

  tags = {
    "Name"               = "integrates.front.production.fluidattacks.com"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
    "Access"             = "private"
  }
}

resource "aws_s3_bucket_acl" "prod" {
  bucket = aws_s3_bucket.prod.id

  acl = "private"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "prod" {
  bucket = aws_s3_bucket.prod.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_cors_configuration" "prod" {
  bucket = aws_s3_bucket.prod.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["GET", "HEAD"]
    max_age_seconds = 3000
  }
}

data "aws_iam_policy_document" "prod" {
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
  policy = data.aws_iam_policy_document.prod.json
}

resource "cloudflare_page_rule" "prod" {
  zone_id  = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  target   = "integrates.front.production.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  status   = "active"
  priority = 1

  actions {
    cache_level       = "aggressive"
    edge_cache_ttl    = 1800
    browser_cache_ttl = 1800
  }
}

resource "cloudflare_record" "prod" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "integrates.front.production.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.prod.bucket_domain_name
  proxied = true
  ttl     = 1
}
