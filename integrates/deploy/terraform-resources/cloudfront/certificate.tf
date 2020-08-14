data "aws_route53_zone" "fluidattacks" {
  name = "fluidattacks.com."
}

resource "aws_acm_certificate" "files-certificate" {
  domain_name       = "files.fluidattacks.com"
  validation_method = "DNS"

lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "files-certificate-validation" {
  name    = aws_acm_certificate.files-certificate.domain_validation_options.0.resource_record_name
  type    = aws_acm_certificate.files-certificate.domain_validation_options.0.resource_record_type
  zone_id = data.aws_route53_zone.fluidattacks.id
  records = [aws_acm_certificate.files-certificate.domain_validation_options.0.resource_record_value]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "files-certificate-validation" {
  certificate_arn         = aws_acm_certificate.files-certificate.arn
  validation_record_fqdns = [aws_route53_record.files-certificate-validation.fqdn]
}

resource "aws_route53_record" "files-alias" {
  zone_id                  =  data.aws_route53_zone.fluidattacks.id
  name                     = "files.fluidattacks.com"
  type                     = "A"
  alias {
    name                   = aws_cloudfront_distribution.fi_reports_cloudfront.domain_name
    zone_id                = aws_cloudfront_distribution.fi_reports_cloudfront.hosted_zone_id
    evaluate_target_health = false
  }
}
