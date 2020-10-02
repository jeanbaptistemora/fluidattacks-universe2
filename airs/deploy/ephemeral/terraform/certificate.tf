resource "aws_acm_certificate" "web-ephemeral-certificate" {
  domain_name       = "web.eph.fluidattacks.com"
  validation_method = "DNS"

lifecycle {
    create_before_destroy = true
  }

  tags = {
    "Name"               = "web-ephemeral-certificate"
    "management:type"    = "development"
    "management:product" = "airs"
  }
}

resource "aws_route53_record" "web-ephemeral-certificate-validation" {
  name    = aws_acm_certificate.web-ephemeral-certificate.domain_validation_options.0.resource_record_name
  type    = aws_acm_certificate.web-ephemeral-certificate.domain_validation_options.0.resource_record_type
  zone_id = data.aws_route53_zone.fluidattacks.id
  records = [aws_acm_certificate.web-ephemeral-certificate.domain_validation_options.0.resource_record_value]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "web-ephemeral-certificate-validation" {
  certificate_arn         = aws_acm_certificate.web-ephemeral-certificate.arn
  validation_record_fqdns = [aws_route53_record.web-ephemeral-certificate-validation.fqdn]
}
