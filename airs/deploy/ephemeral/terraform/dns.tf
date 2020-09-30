resource "aws_route53_record" "web-ephemeral-alias" {
  zone_id = data.aws_route53_zone.fluidattacks.id
  name    = "web.eph.fluidattacks.com"
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.web-ephemeral-distribution.domain_name
    zone_id                = aws_cloudfront_distribution.web-ephemeral-distribution.hosted_zone_id
    evaluate_target_health = false
  }
}
