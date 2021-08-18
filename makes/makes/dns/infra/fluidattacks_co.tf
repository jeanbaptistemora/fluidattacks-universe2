resource "cloudflare_zone" "fluidattacks_co" {
  zone = "fluidattacks.co"
}

resource "cloudflare_zone_settings_override" "fluidattacks_co" {
  zone_id = cloudflare_zone.fluidattacks_co.id

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

resource "cloudflare_zone_dnssec" "fluidattacks_co" {
  zone_id = cloudflare_zone.fluidattacks_co.id
}

# CNAME Records

resource "cloudflare_record" "fluidattacks_co_main" {
  zone_id = cloudflare_zone.fluidattacks_co.id
  name    = cloudflare_zone.fluidattacks_co.zone
  type    = "CNAME"
  value   = "fluidattacks.com"
  proxied = true
}

# Page Rules

resource "cloudflare_page_rule" "fluidattacks_co_to_fluidattacks_com" {
  zone_id  = cloudflare_zone.fluidattacks_co.id
  target   = "${cloudflare_zone.fluidattacks_co.zone}/*"
  status   = "active"
  priority = 1

  actions {
    forwarding_url {
      url         = "https://fluidattacks.com/$1"
      status_code = 301
    }
  }
}

resource "cloudflare_page_rule" "www_fluidattacks_co_to_fluidattacks_com" {
  zone_id  = cloudflare_zone.fluidattacks_co.id
  target   = "www.${cloudflare_zone.fluidattacks_co.zone}/*"
  status   = "active"
  priority = 2

  actions {
    forwarding_url {
      url         = "https://${cloudflare_zone.fluidattacks_co.zone}/$1"
      status_code = 301
    }
  }
}
