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
    tls_1_3                  = "zrt"
    universal_ssl            = "on"
    challenge_ttl            = 1800

    minify {
      css  = "on"
      html = "on"
      js   = "on"
    }

    security_header {
      enabled            = true
      include_subdomains = true
      nosniff            = false
      max_age            = 31536000
      preload            = true
    }
  }
}

resource "cloudflare_zone_dnssec" "fluidattacks_co" {
  zone_id = cloudflare_zone.fluidattacks_co.id
}

# CNAME Records

resource "cloudflare_record" "www_fluidattacks_co" {
  zone_id = cloudflare_zone.fluidattacks_co.id
  name    = "www.${cloudflare_zone.fluidattacks_co.zone}"
  type    = "CNAME"
  value   = cloudflare_zone.fluidattacks_co.zone
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "fluidattacks_co_main" {
  zone_id = cloudflare_zone.fluidattacks_co.id
  name    = cloudflare_zone.fluidattacks_co.zone
  type    = "CNAME"
  value   = "fluidattacks.com"
  proxied = true
}

# Page Rules

resource "cloudflare_page_rule" "fluidattacks_co_http_to_https" {
  zone_id  = cloudflare_zone.fluidattacks_co.id
  target   = "${cloudflare_zone.fluidattacks_co.zone}/*"
  status   = "active"
  priority = 100

  actions {
    always_use_https = true
  }
}

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

resource "cloudflare_page_rule" "redirect_www_http_to_www_https" {
  zone_id  = cloudflare_zone.fluidattacks_co.id
  target   = "www.${cloudflare_zone.fluidattacks_co.zone}/*"
  status   = "active"
  priority = 100

  actions {
    forwarding_url {
      url         = "https://${cloudflare_zone.fluidattacks_co.zone}/$1"
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
