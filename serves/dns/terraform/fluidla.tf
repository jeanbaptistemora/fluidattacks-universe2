resource "cloudflare_zone" "fluid_la" {
  zone = "fluid.la"
}

resource "cloudflare_zone_settings_override" "fluid_la" {
  zone_id = cloudflare_zone.fluid_la.id

  settings {
    always_online            = "on"
    always_use_https         = "on"
    automatic_https_rewrites = "on"
    brotli                   = "on"
    browser_check            = "on"
    cache_level              = "aggressive"
    email_obfuscation        = "on"
    hotlink_protection       = "on"
    ip_geolocation           = "on"
    ipv6                     = "on"
    opportunistic_encryption = "on"
    min_tls_version          = "1.2"
    ssl                      = "flexible"
    tls_1_3                  = "on"
    challenge_ttl            = 1800

    minify {
      css  = "on"
      html = "on"
      js   = "on"
    }

    security_header {
      enabled = true
      max_age = 31536000
    }
  }
}

resource "cloudflare_argo" "fluid_la" {
  zone_id        = cloudflare_zone.fluid_la.id
  tiered_caching = "on"
  smart_routing  = "on"
}

resource "cloudflare_zone_dnssec" "fluid_la" {
  zone_id = cloudflare_zone.fluid_la.id
}

# CNAME Records

resource "cloudflare_record" "fluid_main" {
  zone_id = cloudflare_zone.fluid_la.id
  name    = cloudflare_zone.fluid_la.zone
  type    = "CNAME"
  value   = "fluidattacks.com"
  proxied = true
}