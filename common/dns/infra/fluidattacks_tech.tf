# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "cloudflare_zone" "fluidattacks_tech" {
  zone = "fluidattacks.tech"
}

resource "cloudflare_zone_settings_override" "fluidattacks_tech" {
  zone_id = cloudflare_zone.fluidattacks_tech.id

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

resource "cloudflare_zone_dnssec" "fluidattacks_tech" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
}

# CNAME Recordds

resource "cloudflare_record" "www_fluidattacks_tech" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "www.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = cloudflare_zone.fluidattacks_tech.zone
  proxied = true
}

resource "cloudflare_record" "gd_domainconnect" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "_domainconnect.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "_domainconnect.gd.domaincontrol.com"
  proxied = true
}

resource "cloudflare_record" "secureserver" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "email.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "email.secureserver.net"
  proxied = true
}

resource "cloudflare_record" "godaddy_paylink" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "pay.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "paylinks.commerce.godaddy.com"
  proxied = true
}

resource "cloudflare_record" "mailgun" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "track.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "mailgun.org"
  proxied = true
}

resource "cloudflare_record" "unbounce" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "try.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "CNAME"
  value   = "4aeee6a9e5a245a09a937d23a15e7caf.unbouncepages.com"
  proxied = false
  ttl     = 1
}

# MX Records

resource "cloudflare_record" "mailstore" {
  zone_id  = cloudflare_zone.fluidattacks_tech.id
  name     = cloudflare_zone.fluidattacks_tech.zone
  type     = "MX"
  value    = "mailstore1.secureserver.net"
  ttl      = 1
  proxied  = false
  priority = 1
}

resource "cloudflare_record" "smtp" {
  zone_id  = cloudflare_zone.fluidattacks_tech.id
  name     = cloudflare_zone.fluidattacks_tech.zone
  type     = "MX"
  value    = "smtp.secureserver.net"
  ttl      = 1
  proxied  = false
  priority = 10
}

# SRV Records

resource "cloudflare_record" "autodiscover" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "_autodiscover._tcp"
  type    = "SRV"

  data {
    service  = "_autodiscover"
    proto    = "_tcp"
    name     = "autodiscover-srv"
    priority = 0
    weight   = 0
    port     = 443
    target   = "autodiscover.secureserver.net"
  }
}

# TXT Records

resource "cloudflare_record" "dmarc" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "_dmarc.${cloudflare_zone.fluidattacks_tech.zone}"
  type    = "TXT"
  value   = "v=DMARC1; p=none;"
  ttl     = 1
  proxied = false
}

resource "cloudflare_record" "spoofing" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = cloudflare_zone.fluidattacks_tech.zone
  type    = "TXT"
  value   = "v=spf1 include:mailgun.org ~all"
  ttl     = 1
  proxied = false
}

resource "cloudflare_record" "pic_domainkey" {
  zone_id = cloudflare_zone.fluidattacks_tech.id
  name    = "pic._domainkey"
  type    = "TXT"
  value   = "k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDhlWESKfHJ7mhabvLjIC149sXmbq17kxA/Zivg57SkPtleeANMKK4WbAKl1WtQHnGqSoNsQ8WqoKCPqeSyrc4Sqjg6TJQi7mSq6tNR+gCALB6wSHRoAXwAoOcWkTJTyBUvzZjYaLk4bU7OlykNbYbN6BYudZ7mhIArimrXyttGzwIDAQAB"
  ttl     = 1
  proxied = false
}
