resource "cloudflare_zone" "fluidsignal_com" {
  zone = "fluidsignal.com"
}

resource "cloudflare_zone_settings_override" "fluidsignal" {
  zone_id = cloudflare_zone.fluidsignal_com.id

  settings {
    always_online            = "on"
    always_use_https         = "on"
    automatic_https_rewrites = "on"
    brotli                   = "on"
    browser_check            = "on"
    cache_level              = "basic"
    email_obfuscation        = "on"
    hotlink_protection       = "on"
    ip_geolocation           = "on"
    ipv6                     = "on"
    opportunistic_encryption = "on"
    min_tls_version          = "1.2"
    ssl                      = "strict"
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

resource "cloudflare_record" "fluidsignal_main" {
  zone_id = cloudflare_zone.fluidsignal_com.id
  name    = cloudflare_zone.fluidsignal_com.zone
  type    = "CNAME"
  value   = "fluidattacks.com"
  proxied = true
}

resource "cloudflare_page_rule" "fluidsignal_redirect" {
  zone_id  = cloudflare_zone.fluidsignal_com.id
  target   = "${cloudflare_zone.fluidsignal_com.zone}/*"
  status   = "active"
  priority = 1

  actions {
    forwarding_url {
      url         = "https://fluidattacks.com/$1"
      status_code = 301
    }
  }
}
