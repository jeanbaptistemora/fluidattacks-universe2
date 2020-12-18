# Bucket

resource "aws_s3_bucket" "development" {
  bucket = "integrates.front.development.fluidattacks.com"
  acl    = "private"
  region = var.region

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
    "Name"               = "integrates.front.development.fluidattacks.com"
    "management:type"    = "development"
    "management:product" = "integrates"
  }
}

data "aws_iam_policy_document" "development" {
    statement {
    sid    = "integrates-front-prod"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.development.iam_arn]
    }

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::integrates.front.development.fluidattacks.com/*",
      "arn:aws:s3:::integrates.front.development.fluidattacks.com",
    ]
  }
}

resource "aws_s3_bucket_policy" "development" {
  bucket = aws_s3_bucket.development.id
  policy = data.aws_iam_policy_document.development.json
}


# Certificate

resource "aws_acm_certificate" "development" {
  domain_name       = "integrates.front.development.fluidattacks.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    "Name"               = "integrates-front-development-certificate"
    "management:type"    = "development"
    "management:product" = "integrates"
  }
}

resource "aws_route53_record" "development-validation" {
  name    = aws_acm_certificate.development.domain_validation_options.0.resource_record_name
  type    = aws_acm_certificate.development.domain_validation_options.0.resource_record_type
  zone_id = data.aws_route53_zone.fluidattacks.id
  records = [aws_acm_certificate.development.domain_validation_options.0.resource_record_value]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "development-validation" {
  certificate_arn         = aws_acm_certificate.development.arn
  validation_record_fqdns = [aws_route53_record.development-validation.fqdn]
}


# CloudFront

resource "aws_cloudfront_distribution" "development" {
  origin {
    domain_name = aws_s3_bucket.development.bucket_domain_name
    origin_id   = var.bucket-origin-id-development

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.development.cloudfront_access_identity_path
    }
  }

  enabled             = true
  default_root_object = "index.html"

  aliases = ["integrates.front.development.fluidattacks.com"]

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = var.bucket-origin-id-development

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 60
    max_ttl                = 60
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.development.arn
    minimum_protocol_version = "TLSv1.2_2018"
    ssl_support_method       = "sni-only"
  }

  tags = {
    "Name"               = "integrates-front-development-distribution"
    "management:type"    = "development"
    "management:product" = "integrates"
  }
}

resource "aws_cloudfront_origin_access_identity" "development" {
  comment = "Integrates Front Development"
}

# DNS

resource "aws_route53_record" "development" {
  zone_id = data.aws_route53_zone.fluidattacks.id
  name    = "integrates.front.development.fluidattacks.com"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.development.domain_name
    zone_id                = aws_cloudfront_distribution.development.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "cloudflare_record" "development" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "integrates.front.development.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.development.bucket_domain_name
  proxied = true
  ttl     = 1
}
