resource "cloudflare_zone" "fluidsignal_co" {
  zone = "fluidsignal.co"
}

resource "cloudflare_zone_settings_override" "fluidsignal_co" {
  zone_id = cloudflare_zone.fluidsignal_co.id

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

resource "cloudflare_zone_dnssec" "fluidsignal_co" {
  zone_id = cloudflare_zone.fluidsignal_co.id
}

# CNAME Records

resource "cloudflare_record" "fluidsignal_co_main" {
  zone_id = cloudflare_zone.fluidsignal_co.id
  name    = cloudflare_zone.fluidsignal_co.zone
  type    = "CNAME"
  value   = cloudflare_zone.fluidattacks_com.zone
  proxied = true
}

# Bucket to avoid domain takeover
# https://community.cloudflare.com/t/cloudflare-s3-bucket-with-different-name-bucket-and-domain/193301
resource "aws_s3_bucket" "fluidsignal_co" {
  bucket = "fluidsignal.co"
}
resource "aws_s3_bucket_acl" "fluidsignal_co_acl" {
  bucket = aws_s3_bucket.fluidsignal_co.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "fluidsignal_co_versioning" {
  bucket = aws_s3_bucket.fluidsignal_co.id
  versioning_configuration {
    status = "Suspended"
  }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "fluidsignal_co" {
  bucket = aws_s3_bucket.fluidsignal_co.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}


# MX Records

resource "cloudflare_record" "fluidsignal_co_google_1" {
  zone_id  = cloudflare_zone.fluidsignal_co.id
  name     = cloudflare_zone.fluidsignal_co.zone
  type     = "MX"
  value    = "aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 1
}

resource "cloudflare_record" "fluidsignal_co_google_2" {
  zone_id  = cloudflare_zone.fluidsignal_co.id
  name     = cloudflare_zone.fluidsignal_co.zone
  type     = "MX"
  value    = "alt1.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 5
}

resource "cloudflare_record" "fluidsignal_co_google_3" {
  zone_id  = cloudflare_zone.fluidsignal_co.id
  name     = cloudflare_zone.fluidsignal_co.zone
  type     = "MX"
  value    = "alt2.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 5
}

resource "cloudflare_record" "fluidsignal_co_google_4" {
  zone_id  = cloudflare_zone.fluidsignal_co.id
  name     = cloudflare_zone.fluidsignal_co.zone
  type     = "MX"
  value    = "alt3.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 10
}

resource "cloudflare_record" "fluidsignal_co_google_5" {
  zone_id  = cloudflare_zone.fluidsignal_co.id
  name     = cloudflare_zone.fluidsignal_co.zone
  type     = "MX"
  value    = "alt4.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 10
}

# TXT Records

resource "cloudflare_record" "fluidsignal_co_spf_allowed" {
  zone_id = cloudflare_zone.fluidsignal_co.id
  name    = cloudflare_zone.fluidsignal_co.zone
  type    = "TXT"
  value   = "v=spf1 include:_spf.google.com -all"
  ttl     = 1
  proxied = false
}

resource "cloudflare_record" "fluidsignal_co_verify_google" {
  zone_id = cloudflare_zone.fluidsignal_co.id
  name    = cloudflare_zone.fluidsignal_co.zone
  type    = "TXT"
  value   = "google-site-verification=O1DzXi3E6LIG3nOgpYkkLDU6rELFVMDoO-HPYllLXPw"
  ttl     = 1
  proxied = false
}

# Page Rules

resource "cloudflare_page_rule" "fluidsignal_co_to_fluidattacks_com" {
  zone_id  = cloudflare_zone.fluidsignal_co.id
  target   = "https://${cloudflare_zone.fluidsignal_co.zone}/*"
  status   = "active"
  priority = 1

  actions {
    forwarding_url {
      url         = "https://fluidattacks.com/$1"
      status_code = 301
    }
  }
}

resource "cloudflare_page_rule" "www_fluidsignal_co_to_fluidattacks_com" {
  zone_id  = cloudflare_zone.fluidsignal_co.id
  target   = "https://www.${cloudflare_zone.fluidsignal_co.zone}/*"
  status   = "active"
  priority = 2

  actions {
    forwarding_url {
      url         = "https://${cloudflare_zone.fluidsignal_co.zone}/$1"
      status_code = 301
    }
  }
}
