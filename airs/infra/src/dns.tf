# Production

resource "cloudflare_record" "prod" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")
  type    = "CNAME"
  value   = aws_s3_bucket.prod.website_endpoint
  proxied = true
  ttl     = 1
}


# Development

resource "cloudflare_record" "dev" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "web.eph.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.dev.website_endpoint
  proxied = true
  ttl     = 1
}
