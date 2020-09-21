resource "aws_cloudfront_distribution" "web-ephemeral-distribution" {
  origin {
    domain_name = aws_s3_bucket.web-ephemeral-bucket.bucket_domain_name
    origin_id   = var.bucket-origin-id

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.web-ephemeral-oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  default_root_object = "index.html"

  aliases = ["web.eph.fluidattacks.com"]

  custom_error_response {
    error_code         = "404"
    response_code      = "404"
    response_page_path = "/error-index.html"
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = var.bucket-origin-id

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

    lambda_function_association {
      event_type   = "origin-request"
      lambda_arn   = aws_lambda_function.web-ephemeral-subfolder-to-index.qualified_arn
      include_body = false
    }
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.web-ephemeral-certificate.arn
    minimum_protocol_version = "TLSv1.2_2018"
    ssl_support_method = "sni-only"
  }
}

resource "aws_cloudfront_origin_access_identity" "web-ephemeral-oai" {
  comment = "Web Ephemeral"
}
