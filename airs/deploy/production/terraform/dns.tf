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

resource "cloudflare_record" "fluidattacks_com" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "web.eph.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.bucket.bucket_domain_name
  proxied = true
  ttl     = 1
}
