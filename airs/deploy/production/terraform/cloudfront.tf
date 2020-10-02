resource "aws_cloudfront_distribution" "production" {
  origin {
    domain_name = aws_s3_bucket.bucket.bucket_domain_name
    origin_id   = var.bucket_origin_id

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.production.cloudfront_access_identity_path
    }
  }

  enabled             = true
  default_root_object = "index.html"

  aliases = ["fluidattacks.com"]

  custom_error_response {
    error_code         = "404"
    response_code      = "404"
    response_page_path = "/error/index.html"
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = var.bucket_origin_id

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
      lambda_arn   = aws_lambda_function.subfolder_to_index.qualified_arn
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
    acm_certificate_arn = var.fluidattacks_root_certificate_arn
    minimum_protocol_version = "TLSv1.2_2018"
    ssl_support_method = "sni-only"
  }

  tags = {
    "Name"               = "web-production-distribution"
    "management:type"    = "production"
    "management:product" = "airs"
  }
}

resource "aws_cloudfront_origin_access_identity" "production" {
  comment = "Web Production"
}
