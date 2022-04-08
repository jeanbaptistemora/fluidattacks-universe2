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

resource "cloudflare_zone_dnssec" "fluid_la" {
  zone_id = cloudflare_zone.fluid_la.id
}

# CNAME Records

resource "cloudflare_record" "fluid_la_main" {
  zone_id = cloudflare_zone.fluid_la.id
  name    = cloudflare_zone.fluid_la.zone
  type    = "CNAME"
  value   = "fluidattacks.com"
  proxied = true
}

# MX Records

resource "cloudflare_record" "fluid_la_email_1" {
  zone_id  = cloudflare_zone.fluid_la.id
  name     = cloudflare_zone.fluid_la.zone
  type     = "MX"
  priority = 1
  value    = "aspmx.l.google.com"
  ttl      = 300
}

resource "cloudflare_record" "fluid_la_email_2" {
  zone_id  = cloudflare_zone.fluid_la.id
  name     = cloudflare_zone.fluid_la.zone
  type     = "MX"
  priority = 5
  value    = "alt1.aspmx.l.google.com"
  ttl      = 300
}

resource "cloudflare_record" "fluid_la_email_3" {
  zone_id  = cloudflare_zone.fluid_la.id
  name     = cloudflare_zone.fluid_la.zone
  type     = "MX"
  priority = 5
  value    = "alt2.aspmx.l.google.com"
  ttl      = 300
}

resource "cloudflare_record" "fluid_la_email_4" {
  zone_id  = cloudflare_zone.fluid_la.id
  name     = cloudflare_zone.fluid_la.zone
  type     = "MX"
  priority = 10
  value    = "aspmx2.googlemail.com"
  ttl      = 300
}

resource "cloudflare_record" "fluid_la_email_5" {
  zone_id  = cloudflare_zone.fluid_la.id
  name     = cloudflare_zone.fluid_la.zone
  type     = "MX"
  priority = 10
  value    = "aspmx3.googlemail.com"
  ttl      = 300
}

# TXT Records

resource "cloudflare_record" "mail_dkim_1" {
  zone_id = cloudflare_zone.fluid_la.id
  name    = "google._domainkey.${cloudflare_zone.fluid_la.zone}"
  type    = "TXT"
  value   = "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx+xoz9Br2pk6tPeDrPV/uj7SdMNw9JpxurqL6w1o2f24S4X+QBSR/JaVKoh2FnFj56b9U4R4vWD4aeYk/U5Mwm6AyeXFw/yMG1HwkHDRAna2/gII69ZcH2M+oSCWZwf0IkYT6oyZch7mpFDy5sU26cWWhi+p10mslmpp02eQbMs2fTM9WxlfOiA4kD9BujFSafhW/yHcUpXVQKoVp+C26ZvmM7hNvK++HoWLxOFtVoxje6zfiE86G1SbXKCuufmcJnjva8K2nYW07qYZAgftBGXJUZTYLYkrMWYK4q4ghcsgJY9zBQpZmFfRcTvoLhZso8SZmt6Q7Rcvs/8isuzb7wIDAQAB"
  ttl     = 1
  proxied = false
}

# Page Rules

resource "cloudflare_page_rule" "fluidla_to_fluidattacks_com" {
  zone_id  = cloudflare_zone.fluid_la.id
  target   = "${cloudflare_zone.fluid_la.zone}/*"
  status   = "active"
  priority = 1

  actions {
    forwarding_url {
      url         = "https://fluidattacks.com/$1"
      status_code = 301
    }
  }
}

resource "cloudflare_page_rule" "www_fluidla_to_fluidattacks_com" {
  zone_id  = cloudflare_zone.fluid_la.id
  target   = "www.${cloudflare_zone.fluid_la.zone}/*"
  status   = "active"
  priority = 2

  actions {
    forwarding_url {
      url         = "https://${cloudflare_zone.fluid_la.zone}/$1"
      status_code = 301
    }
  }
}
