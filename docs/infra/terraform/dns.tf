# Production

resource "cloudflare_record" "doc_prod" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "docs.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.bucket_prod.website_endpoint
  proxied = true
  ttl     = 1
}


# Development

resource "cloudflare_record" "doc_dev" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "docs-dev.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.bucket_dev.website_endpoint
  proxied = true
  ttl     = 1
}
