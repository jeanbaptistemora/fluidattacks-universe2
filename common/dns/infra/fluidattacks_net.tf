resource "cloudflare_zone" "fluidattacks_net" {
  zone = "fluidattacks.net"
}

resource "cloudflare_zone_settings_override" "fluidattacks_net" {
  zone_id = cloudflare_zone.fluidattacks_net.id

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

resource "cloudflare_zone_dnssec" "fluidattacks_net" {
  zone_id = cloudflare_zone.fluidattacks_net.id
}

# CNAME Records

resource "cloudflare_record" "fluidattacks_net_main" {
  zone_id = cloudflare_zone.fluidattacks_net.id
  name    = cloudflare_zone.fluidattacks_net.zone
  type    = "CNAME"
  value   = "fluidattacks.com"
  proxied = true
}

# Bucket to avoid domain takeover
# https://community.cloudflare.com/t/cloudflare-s3-bucket-with-different-name-bucket-and-domain/193301
resource "aws_s3_bucket" "fluidattacks_net" {
  bucket = "fluidattacks.net"
}
resource "aws_s3_bucket_acl" "fluidattacks_net_acl" {
  bucket = aws_s3_bucket.fluidattacks_net.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "fluidattacks_net_versioning" {
  bucket = aws_s3_bucket.fluidattacks_net.id
  versioning_configuration {
    status = "Suspended"
  }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "fluidattacks_net" {
  bucket = aws_s3_bucket.fluidattacks_net.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}


# MX Records

resource "cloudflare_record" "fluidattacks_net_google_1" {
  zone_id  = cloudflare_zone.fluidattacks_net.id
  name     = cloudflare_zone.fluidattacks_net.zone
  type     = "MX"
  value    = "aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 1
}

resource "cloudflare_record" "fluidattacks_net_google_2" {
  zone_id  = cloudflare_zone.fluidattacks_net.id
  name     = cloudflare_zone.fluidattacks_net.zone
  type     = "MX"
  value    = "alt1.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 5
}

resource "cloudflare_record" "fluidattacks_net_google_3" {
  zone_id  = cloudflare_zone.fluidattacks_net.id
  name     = cloudflare_zone.fluidattacks_net.zone
  type     = "MX"
  value    = "alt2.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 5
}

resource "cloudflare_record" "fluidattacks_net_google_4" {
  zone_id  = cloudflare_zone.fluidattacks_net.id
  name     = cloudflare_zone.fluidattacks_net.zone
  type     = "MX"
  value    = "alt3.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 10
}

resource "cloudflare_record" "fluidattacks_net_google_5" {
  zone_id  = cloudflare_zone.fluidattacks_net.id
  name     = cloudflare_zone.fluidattacks_net.zone
  type     = "MX"
  value    = "alt4.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 10
}

# TXT Records

resource "cloudflare_record" "fluidattacks_net_spf_allowed" {
  zone_id = cloudflare_zone.fluidattacks_net.id
  name    = cloudflare_zone.fluidattacks_net.zone
  type    = "TXT"
  value   = "v=spf1 include:_spf.google.com -all"
  ttl     = 1
  proxied = false
}

resource "cloudflare_record" "fluidattacks_net_verify_google" {
  zone_id = cloudflare_zone.fluidattacks_net.id
  name    = cloudflare_zone.fluidattacks_net.zone
  type    = "TXT"
  value   = "google-site-verification=O1DzXi3E6LIG3nOgpYkkLDU6rELFVMDoO-HPYllLXPw"
  ttl     = 1
  proxied = false
}

# Page Rules

resource "cloudflare_page_rule" "fluidattacks_net_to_fluidattacks_netm" {
  zone_id  = cloudflare_zone.fluidattacks_net.id
  target   = "https://${cloudflare_zone.fluidattacks_net.zone}/*"
  status   = "active"
  priority = 1

  actions {
    forwarding_url {
      url         = "https://fluidattacks.com/$1"
      status_code = 301
    }
  }
}

resource "cloudflare_page_rule" "www_fluidattacks_net_to_fluidattacks_net" {
  zone_id  = cloudflare_zone.fluidattacks_net.id
  target   = "https://www.${cloudflare_zone.fluidattacks_net.zone}/*"
  status   = "active"
  priority = 2

  actions {
    forwarding_url {
      url         = "https://${cloudflare_zone.fluidattacks_net.zone}/$1"
      status_code = 301
    }
  }
}
