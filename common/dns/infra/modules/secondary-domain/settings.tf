resource "cloudflare_zone" "main" {
  account_id = var.cloudflareAccountId
  zone       = var.domain
}

resource "cloudflare_zone_settings_override" "main" {
  zone_id = cloudflare_zone.main.id

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

resource "cloudflare_zone_dnssec" "main" {
  zone_id = cloudflare_zone.main.id
}
