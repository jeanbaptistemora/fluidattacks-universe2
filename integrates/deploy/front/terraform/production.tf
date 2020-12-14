
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
