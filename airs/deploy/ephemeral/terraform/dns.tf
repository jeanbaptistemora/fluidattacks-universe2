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

resource "cloudflare_record" "web-ephemeral-alias" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "web.eph.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.web-ephemeral-bucket.bucket_domain_name
  proxied = true
  ttl     = 1
}
