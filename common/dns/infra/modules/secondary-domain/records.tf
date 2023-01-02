# CNAME Records

resource "cloudflare_record" "main" {
  zone_id = cloudflare_zone.main.id
  name    = cloudflare_zone.main.zone
  type    = "CNAME"
  value   = "fluidattacks.com"
  proxied = true
}

# MX Records

resource "cloudflare_record" "main_google_1" {
  zone_id  = cloudflare_zone.main.id
  name     = cloudflare_zone.main.zone
  type     = "MX"
  value    = "aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 1
}

resource "cloudflare_record" "main_google_2" {
  zone_id  = cloudflare_zone.main.id
  name     = cloudflare_zone.main.zone
  type     = "MX"
  value    = "alt1.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 5
}

resource "cloudflare_record" "main_google_3" {
  zone_id  = cloudflare_zone.main.id
  name     = cloudflare_zone.main.zone
  type     = "MX"
  value    = "alt2.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 5
}

resource "cloudflare_record" "main_google_4" {
  zone_id  = cloudflare_zone.main.id
  name     = cloudflare_zone.main.zone
  type     = "MX"
  value    = "alt3.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 10
}

resource "cloudflare_record" "main_google_5" {
  zone_id  = cloudflare_zone.main.id
  name     = cloudflare_zone.main.zone
  type     = "MX"
  value    = "alt4.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 10
}

# TXT Records

resource "cloudflare_record" "main_spf_allowed" {
  zone_id = cloudflare_zone.main.id
  name    = cloudflare_zone.main.zone
  type    = "TXT"
  value   = "v=spf1 include:_spf.google.com -all"
  ttl     = 1
  proxied = false
}

resource "cloudflare_record" "main_verify_google" {
  zone_id = cloudflare_zone.main.id
  name    = cloudflare_zone.main.zone
  type    = "TXT"
  value   = "google-site-verification=O1DzXi3E6LIG3nOgpYkkLDU6rELFVMDoO-HPYllLXPw"
  ttl     = 1
  proxied = false
}
