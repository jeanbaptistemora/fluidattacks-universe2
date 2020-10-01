resource "aws_route53_record" "fluidattacks_com" {
  zone_id = data.aws_route53_zone.fluidattacks.id
  name    = "fluidattacks.com"
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.production.domain_name
    zone_id                = aws_cloudfront_distribution.production.hosted_zone_id
    evaluate_target_health = false
  }
}
