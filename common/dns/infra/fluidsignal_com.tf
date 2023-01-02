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

resource "cloudflare_argo" "fluidsignal_com" {
  zone_id        = cloudflare_zone.fluidsignal_com.id
  tiered_caching = "on"
  smart_routing  = "on"
}

resource "cloudflare_zone_dnssec" "fluidsignal_com" {
  zone_id = cloudflare_zone.fluidsignal_com.id
}


# CNAME Records

resource "cloudflare_record" "fluidsignal_main" {
  zone_id = cloudflare_zone.fluidsignal_com.id
  name    = cloudflare_zone.fluidsignal_com.zone
  type    = "CNAME"
  value   = cloudflare_zone.fluidattacks_com.zone
  proxied = true
}

# Bucket to avoid domain takeover
# https://community.cloudflare.com/t/cloudflare-s3-bucket-with-different-name-bucket-and-domain/193301
resource "aws_s3_bucket" "fluidsignal_com" {
  bucket = "fluidsignal.com"
}
resource "aws_s3_bucket_acl" "fluidsignal_com_acl" {
  bucket = aws_s3_bucket.fluidsignal_com.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "fluidsignal_com_versioning" {
  bucket = aws_s3_bucket.fluidsignal_com.id
  versioning_configuration {
    status = "Suspended"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "fluidsignal_com" {
  bucket = aws_s3_bucket.fluidsignal_com.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}


# MX Records

resource "cloudflare_record" "fluidsignal_com_email_1" {
  zone_id  = cloudflare_zone.fluidsignal_com.id
  name     = cloudflare_zone.fluidsignal_com.zone
  type     = "MX"
  priority = 1
  value    = "aspmx.l.google.com"
  ttl      = 300
}

resource "cloudflare_record" "fluidsignal_com_email_2" {
  zone_id  = cloudflare_zone.fluidsignal_com.id
  name     = cloudflare_zone.fluidsignal_com.zone
  type     = "MX"
  priority = 5
  value    = "alt1.aspmx.l.google.com"
  ttl      = 300
}

resource "cloudflare_record" "fluidsignal_com_email_3" {
  zone_id  = cloudflare_zone.fluidsignal_com.id
  name     = cloudflare_zone.fluidsignal_com.zone
  type     = "MX"
  priority = 5
  value    = "alt2.aspmx.l.google.com"
  ttl      = 300
}

resource "cloudflare_record" "fluidsignal_com_email_4" {
  zone_id  = cloudflare_zone.fluidsignal_com.id
  name     = cloudflare_zone.fluidsignal_com.zone
  type     = "MX"
  priority = 10
  value    = "aspmx2.googlemail.com"
  ttl      = 300
}

resource "cloudflare_record" "fluidsignal_com_email_5" {
  zone_id  = cloudflare_zone.fluidsignal_com.id
  name     = cloudflare_zone.fluidsignal_com.zone
  type     = "MX"
  priority = 10
  value    = "aspmx3.googlemail.com"
  ttl      = 300
}


# Page Rules

resource "cloudflare_page_rule" "fluidsignal_com_to_fluidattacks_com" {
  zone_id  = cloudflare_zone.fluidsignal_com.id
  target   = "https://${cloudflare_zone.fluidsignal_com.zone}/*"
  status   = "active"
  priority = 1

  actions {
    forwarding_url {
      url         = "https://fluidattacks.com/$1"
      status_code = 301
    }
  }
}

resource "cloudflare_page_rule" "www_fluidsignal_com_to_fluidattacks_com" {
  zone_id  = cloudflare_zone.fluidsignal_com.id
  target   = "https://www.${cloudflare_zone.fluidsignal_com.zone}/*"
  status   = "active"
  priority = 2

  actions {
    forwarding_url {
      url         = "https://fluidattacks.com/$1"
      status_code = 301
    }
  }
}
