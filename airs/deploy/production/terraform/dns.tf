resource "cloudflare_record" "fluidattacks_com" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")
  type    = "CNAME"
  value   = aws_s3_bucket.bucket.website_endpoint
  proxied = true
  ttl     = 1
}
