# Production

resource "cloudflare_record" "doc_prod" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "docs.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = aws_s3_bucket.bucket_prod.website_endpoint
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "doc" {
  zone_id = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  name    = "doc.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  type    = "CNAME"
  value   = "docs.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}"
  proxied = true
  ttl     = 1
}

resource "cloudflare_page_rule" "redirect_doc" {
  zone_id  = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  target   = "doc.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  status   = "active"
  priority = 99

  actions {
    forwarding_url {
      url         = "https://docs.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/$1"
      status_code = 301
    }
  }
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
