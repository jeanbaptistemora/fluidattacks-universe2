resource "aws_acm_certificate" "ephemeral" {
  domain_name       = "*.integrates.fluidattacks.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    "management:type"    = "development"
    "management:product" = "integrates"
  }
}

resource "aws_route53_record" "ephemeral" {
  for_each = {
    for dvo in aws_acm_certificate.ephemeral.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }
  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.fluidattacks.id
}

resource "aws_acm_certificate_validation" "ephemeral" {
  certificate_arn         = aws_acm_certificate.ephemeral.arn
  validation_record_fqdns = [ for record in aws_route53_record.ephemeral : record.fqdn ]
}
