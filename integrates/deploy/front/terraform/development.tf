# Bucket
resource "aws_s3_bucket" "development" {
  bucket = "integrates.front.dev.fluidattacks.com"
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
    "Name"               = "integrates.front.dev.fluidattacks.com"
    "management:type"    = "development"
    "management:product" = "integrates"
  }
}

# Certificate
resource "aws_acm_certificate" "development" {
  domain_name       = "integrates.front.dev.fluidattacks.com"
  validation_method = "DNS"

lifecycle {
    create_before_destroy = true
  }

  tags = {
    "Name"               = "integrates-front-dev-certificate"
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
