# Bucket

resource "aws_s3_bucket" "development" {
  bucket = "integrates.front.development.fluidattacks.com"
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
    "Name"            = "integrates.front.development.fluidattacks.com"
    "management:area" = "innovation"
    "management:type" = "product"
  }
}

data "aws_iam_policy_document" "development" {
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
      "${aws_s3_bucket.development.arn}/*",
    ]
    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "development" {
  bucket = aws_s3_bucket.development.id
  policy = data.aws_iam_policy_document.development.json
}


# Cache

resource "cloudflare_page_rule" "development" {
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


# DNS

resource "cloudflare_record" "development" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "integrates.front.development.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.development.bucket_domain_name
  proxied = true
  ttl     = 1
}
