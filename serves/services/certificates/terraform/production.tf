resource "aws_acm_certificate" "production" {
  domain_name       = "*.fluidattacks.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    "Name"               = "production"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_route53_record" "production" {
  for_each = {
    for dvo in aws_acm_certificate.production.domain_validation_options : dvo.domain_name => {
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

resource "aws_acm_certificate_validation" "production" {
  certificate_arn         = aws_acm_certificate.production.arn
  validation_record_fqdns = [for record in aws_route53_record.production : record.fqdn]
}

resource "aws_acm_certificate" "root" {
  domain_name       = "fluidattacks.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    "Name"               = "root"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_route53_record" "root" {
  depends_on = [aws_acm_certificate.root]

  for_each = {
    for dvo in aws_acm_certificate.root.domain_validation_options : dvo.domain_name => {
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

resource "aws_acm_certificate_validation" "root" {
  depends_on = [aws_route53_record.root]

  certificate_arn         = aws_acm_certificate.root.arn
  validation_record_fqdns = [for record in aws_route53_record.root : record.fqdn]
}
