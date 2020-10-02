resource "aws_cloudfront_origin_access_identity" "cloudfront_identity" {
  comment = "Integrates resources"
}

resource "aws_cloudfront_distribution" "fi_resources_cloudfront" {
  enabled             = true
  is_ipv6_enabled     = true
  http_version        = "http2"
  price_class         = "PriceClass_All"
  retain_on_delete    = false
  wait_for_deployment = true

  tags = {
    "Name"               = "fi_resources_cloudfront"
    "management:type"    = "production"
    "management:product" = "integrates"
  }

  origin {
    origin_id = "S3-fluidintegrates.resources"
    domain_name = aws_s3_bucket.fi_resources_bucket.bucket_domain_name

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.cloudfront_identity.cloudfront_access_identity_path
    }
  }

  origin {
    origin_id   = "S3-fluidintegrates.evidences"
    domain_name = aws_s3_bucket.fi_evidences_bucket.bucket_domain_name

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.cloudfront_identity.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    target_origin_id       = "S3-fluidintegrates.resources"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
    smooth_streaming       = false

    allowed_methods = [
      "GET",
      "HEAD"
    ]
    cached_methods  = [
      "GET",
      "HEAD"
    ]
    trusted_signers = [
      "self"
    ]

    forwarded_values {
      query_string = false

      cookies {
        forward    = "none"
      }
    }
  }

  ordered_cache_behavior {
    path_pattern           = "/*/*/*"
    target_origin_id       = "S3-fluidintegrates.evidences"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
    smooth_streaming       = false

    allowed_methods = [
      "GET",
      "HEAD"
    ]
    cached_methods  = [
      "GET",
      "HEAD"
    ]
    trusted_signers = [
      "self"
    ]

    forwarded_values {
      query_string = false

      cookies {
        forward    = "none"
      }
    }
  }

  custom_error_response {
    error_code = 404
    error_caching_min_ttl = 0
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
    minimum_protocol_version       = "TLSv1.2_2018"
  }
}

resource "aws_cloudfront_distribution" "fi_reports_cloudfront" {
  enabled             = true
  is_ipv6_enabled     = true
  http_version        = "http2"
  price_class         = "PriceClass_All"
  retain_on_delete    = false
  wait_for_deployment = true

  tags = {
    "Name"               = "fi_reports_cloudfront"
    "management:type"    = "production"
    "management:product" = "integrates"
  }

  origin {
    origin_id = "S3-fluidintegrates.reports"
    domain_name = aws_s3_bucket.fi_reports_bucket.bucket_domain_name

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.cloudfront_identity.cloudfront_access_identity_path
    }
  }

  aliases = ["files.fluidattacks.com"]

  default_cache_behavior {
    target_origin_id       = "S3-fluidintegrates.reports"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
    smooth_streaming       = false

    allowed_methods = [
      "GET",
      "HEAD"
    ]
    cached_methods  = [
      "GET",
      "HEAD"
    ]
    trusted_signers = [
      "self"
    ]

    forwarded_values {
      query_string = false

      cookies {
        forward    = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.files-certificate.arn
    minimum_protocol_version = "TLSv1.2_2018"
    ssl_support_method = "sni-only"
  }
}
