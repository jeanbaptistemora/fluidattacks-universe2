# Bucket

resource "aws_s3_bucket" "production" {
  bucket = "integrates.front.production.fluidattacks.com"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["GET", "HEAD"]
    max_age_seconds = 3000
  }

  versioning {
    enabled = false
  }

  tags = {
    "Name"               = "integrates.front.production.fluidattacks.com"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

data "aws_iam_policy_document" "production" {
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
      "${aws_s3_bucket.production.arn}/*",
    ]
    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "production" {
  bucket = aws_s3_bucket.production.id
  policy = data.aws_iam_policy_document.production.json
}


# Cache

resource "cloudflare_page_rule" "production" {
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


# DNS

resource "cloudflare_record" "production" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "integrates.front.production.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.production.bucket_domain_name
  proxied = true
  ttl     = 1
}
