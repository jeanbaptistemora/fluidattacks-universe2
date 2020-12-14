
# Bucket
resource "aws_s3_bucket" "production" {
  bucket = "integrates.front.prod.fluidattacks.com"
  acl    = "private"
  region = var.region

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  versioning {
    enabled = false
  }

  tags = {
    "Name"               = "integrates.front.prod.fluidattacks.com"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

data "aws_iam_policy_document" "production" {
    statement {
    sid    = "integrates-front-prod"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.production.iam_arn]
    }

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::integrates.front.prod.fluidattacks.com/*",
      "arn:aws:s3:::integrates.front.prod.fluidattacks.com",
    ]
  }
}

resource "aws_s3_bucket_policy" "production" {
  bucket = aws_s3_bucket.production.id
  policy = data.aws_iam_policy_document.production.json
}


# Certificate

resource "aws_acm_certificate" "production" {
  domain_name       = "integrates.front.prod.fluidattacks.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    "Name"               = "integrates-front-prod-certificate"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_route53_record" "production-validation" {
  name    = aws_acm_certificate.production.domain_validation_options.0.resource_record_name
  type    = aws_acm_certificate.production.domain_validation_options.0.resource_record_type
  zone_id = data.aws_route53_zone.fluidattacks.id
  records = [aws_acm_certificate.production.domain_validation_options.0.resource_record_value]
  ttl     = 60
}
resource "aws_acm_certificate_validation" "production-validation" {
  certificate_arn         = aws_acm_certificate.production.arn
  validation_record_fqdns = [aws_route53_record.production-validation.fqdn]
}


# CloudFront

resource "aws_cloudfront_distribution" "production" {
  origin {
    domain_name = aws_s3_bucket.production.bucket_domain_name
    origin_id   = var.bucket-origin-id-prod

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.production.cloudfront_access_identity_path
    }
  }

  enabled             = true
  default_root_object = "index.html"

  aliases = ["integrates.front.prod.fluidattacks.com"]

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = var.bucket-origin-id-prod

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
    acm_certificate_arn      = aws_acm_certificate.production.arn
    minimum_protocol_version = "TLSv1.2_2018"
    ssl_support_method       = "sni-only"
  }

  tags = {
    "Name"               = "integrates-front-prod-distribution"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_cloudfront_origin_access_identity" "production" {
  comment = "Integrates Front Production"
}


# DNS

resource "aws_route53_record" "production" {
  zone_id = data.aws_route53_zone.fluidattacks.id
  name    = "integrates.front.prod.fluidattacks.com"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.production.domain_name
    zone_id                = aws_cloudfront_distribution.production.hosted_zone_id
    evaluate_target_health = false
  }
}
