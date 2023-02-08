resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name = aws_s3_bucket.primary.bucket_regional_domain_name
    origin_id   = "primaryS3"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.default.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    # ... other configuration ...
    target_origin_id = "groupS3"
  }

  logging_config {
    bucket = "myawslogbucket.s3.amazonaws.com"
  }

  # ... other configuration ...
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name = aws_s3_bucket.primary.bucket_regional_domain_name
    origin_id   = "primaryS3"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.default.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    # ... other configuration ...
    target_origin_id = "groupS3"
  }

  # ... other configuration ...
}
