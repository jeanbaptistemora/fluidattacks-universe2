resource "cloudflare_zone" "fluidattacks_com" {
  zone = "fluidattacks.com"
}

resource "cloudflare_zone_settings_override" "fluidattacks_com" {
  zone_id = cloudflare_zone.fluidattacks_com.id

  settings {
    always_online               = "on"
    always_use_https            = "on"
    automatic_https_rewrites    = "on"
    brotli                      = "on"
    browser_cache_ttl           = 1800
    browser_check               = "on"
    cache_level                 = "aggressive"
    challenge_ttl               = 1800
    cname_flattening            = "flatten_at_root"
    development_mode            = "off"
    email_obfuscation           = "on"
    h2_prioritization           = "on"
    hotlink_protection          = "on"
    http2                       = "on"
    http3                       = "on"
    image_resizing              = "off"
    ip_geolocation              = "on"
    ipv6                        = "on"
    max_upload                  = 100
    min_tls_version             = "1.2"
    mirage                      = "on"
    opportunistic_encryption    = "on"
    opportunistic_onion         = "on"
    origin_error_page_pass_thru = "off"
    polish                      = "lossy"
    pseudo_ipv4                 = "off"
    prefetch_preload            = "off"
    privacy_pass                = "on"
    response_buffering          = "off"
    rocket_loader               = "off"
    security_level              = "medium"
    server_side_exclude         = "on"
    sort_query_string_for_cache = "off"
    ssl                         = "flexible"
    tls_1_3                     = "zrt"
    tls_client_auth             = "off"
    true_client_ip_header       = "off"
    universal_ssl               = "on"
    waf                         = "on"
    webp                        = "on"
    websockets                  = "on"
    zero_rtt                    = "on"

    minify {
      css  = "on"
      html = "on"
      js   = "on"
    }

    security_header {
      enabled            = true
      preload            = false
      include_subdomains = false
      nosniff            = false
      max_age            = 31536000
    }
  }
}

resource "cloudflare_rate_limit" "fluidattacks_com" {
  zone_id             = cloudflare_zone.fluidattacks_com.id
  threshold           = 500
  period              = 60
  disabled            = false
  description         = "Main rate limit"
  bypass_url_patterns = []

  match {
    request {
      url_pattern = "*"
      schemes     = ["_ALL_"]
      methods     = ["_ALL_"]
    }
    response {
      origin_traffic = true
    }
  }

  action {
    mode = "simulate"
    timeout = 3600
  }

  correlate {
    by = "nat"
  }
}

resource "cloudflare_argo" "fluidattacks_com" {
  zone_id        = cloudflare_zone.fluidattacks_com.id
  tiered_caching = "on"
  smart_routing  = "on"
}

resource "cloudflare_zone_dnssec" "fluidattacks_com" {
  zone_id = cloudflare_zone.fluidattacks_com.id
}


# CNAME Records

resource "cloudflare_record" "www" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "www.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = cloudflare_zone.fluidattacks_com.zone
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "landing" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "landing.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "a2cbfad5d1d14c9eb6099182bb1adb48.unbouncepages.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "landing_usa" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "usa.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "60afa14d825c49689b84f58f10773196.unbouncepages.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "landing_report2020" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "report2020.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "64b61b566e6b494db43ea4242748637a.unbouncepages.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "track" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "track.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "mandrillapp.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "mailchimp_domainkey_1" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "k1._domainkey.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "dkim.mcsv.net"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "mailchimp_domainkey_2" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "k2._domainkey.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "dkim2.mcsv.net"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "mailchimp_domainkey_3" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "k3._domainkey.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "dkim3.mcsv.net"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "zoho_verify_directory" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "zb62268970.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "zmverify.zoho.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "mail" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "mail.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "ghs.googlehosted.com"
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "status" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "status.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "dashboards.checklyhq.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "news" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "news.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "cname.announcekit.app"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "help" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "help.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "fluidattacks.zendesk.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "rebrandly" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "go.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "rebrandlydomain.com"
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "zoho_desk" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "help2.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "desk.cs.zohohost.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "discourse" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "community.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "fluidattacks.hosted-by-discourse.com"
  proxied = false
  ttl     = 1
}

resource "cloudflare_record" "zd1_domainkey" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "zendesk1.domainkey.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "zendesk1.domainkey.zendesk.com"
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "zd2_domainkey" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "zendesk2.domainkey.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "zendesk2.domainkey.zendesk.com"
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "zd_mail1" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "zendesk1.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "mail1.zendesk.com"
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "zd_mail2" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "zendesk2.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "mail2.zendesk.com"
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "zd_mail3" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "zendesk3.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "mail3.zendesk.com"
  proxied = true
  ttl     = 1
}

resource "cloudflare_record" "zd_mail4" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "zendesk4.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "CNAME"
  value   = "mail4.zendesk.com"
  proxied = true
  ttl     = 1
}


# MX Records

resource "cloudflare_record" "gmail_1" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = cloudflare_zone.fluidattacks_com.zone
  type     = "MX"
  value    = "aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 1
}

resource "cloudflare_record" "gmail_2" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = cloudflare_zone.fluidattacks_com.zone
  type     = "MX"
  value    = "alt1.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 5
}

resource "cloudflare_record" "gmail_3" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = cloudflare_zone.fluidattacks_com.zone
  type     = "MX"
  value    = "alt2.aspmx.l.google.com"
  ttl      = 1
  proxied  = false
  priority = 5
}

resource "cloudflare_record" "gmail_4" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = cloudflare_zone.fluidattacks_com.zone
  type     = "MX"
  value    = "aspmx2.googlemail.com"
  ttl      = 1
  proxied  = false
  priority = 10
}

resource "cloudflare_record" "gmail_5" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = cloudflare_zone.fluidattacks_com.zone
  type     = "MX"
  value    = "aspmx3.googlemail.com"
  ttl      = 1
  proxied  = false
  priority = 10
}

resource "cloudflare_record" "mailgun_1" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = "mailgun.${cloudflare_zone.fluidattacks_com.zone}"
  type     = "MX"
  value    = "mxa.mailgun.org"
  ttl      = 1
  proxied  = false
  priority = 10
}

resource "cloudflare_record" "mailgun_2" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = "mailgun.${cloudflare_zone.fluidattacks_com.zone}"
  type     = "MX"
  value    = "mxb.mailgun.org"
  ttl      = 1
  proxied  = false
  priority = 10
}


# TXT Records

resource "cloudflare_record" "spf_allowed" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = cloudflare_zone.fluidattacks_com.zone
  type     = "TXT"
  value    = "v=spf1 include:_spf.google.com include:mail.zendesk.com include:spf.mandrillapp.com include:servers.mcsv.net include:transmail.net -all"
  ttl      = 1
  proxied  = false
}

resource "cloudflare_record" "verify_zendesk" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = "zendeskverification.${cloudflare_zone.fluidattacks_com.zone}"
  type     = "TXT"
  value    = "27f6e2e3b646cce6"
  ttl      = 1
  proxied  = false
}

resource "cloudflare_record" "verify_google_1" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = cloudflare_zone.fluidattacks_com.zone
  type     = "TXT"
  value    = "google-site-verification=SK6CMgAtuuw7tR6eCev6XY8D6rjn9BW8AGd5KWS1b5g"
  ttl      = 1
  proxied  = false
}

resource "cloudflare_record" "verify_google_2" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = cloudflare_zone.fluidattacks_com.zone
  type     = "TXT"
  value    = "google-site-verification=zVcDOWOKonibpIrLLyFEuy8jbpTJyOPiA39vngIpEvI"
  ttl      = 1
  proxied  = false
}

resource "cloudflare_record" "mail_dmarc" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = "_dmarc.${cloudflare_zone.fluidattacks_com.zone}"
  type     = "TXT"
  value    = "v=DMARC1; p=quarantine; rua=mailto:technology+dmarc@fluidattacks.com"
  ttl      = 1
  proxied  = false
}

resource "cloudflare_record" "mail_dkim" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = "google._domainkey.${cloudflare_zone.fluidattacks_com.zone}"
  type     = "TXT"
  value    = "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoVfDxzz1BbwFFyeQvKe7B4YMSR1HWmjCu4PQzESyAAc9XQDSbtoYQNCHaHisTJNgh4OGEWvgRcpsVljffC5jO3tHcra8xW8ls5O16sClQtfitcKhC1VxNbqYoAnUSNv9FBcsldK96jQgeMrsZUMo6SdldCDO\"\"kX7vOjgLzDw6dOMAENSoU3NsMfRwoDaanCf2gkFb+5mOtDUZCHukM5rpj+ePc3GJAzX8bakMdWD7BlZnPT0fRVcSQGOAM1GVcSDYR465hdBkADJg3KM2TdPTC/XLwEQXgqRZXVWMtSu/Rb/DcHILZNmzKxUk/B4eKjXGQDbs9hshgsqsZGYEbhOvrwIDAQAB"
  ttl      = 1
  proxied  = false
}

resource "cloudflare_record" "mandrill_dkim" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = "mandrill._domainkey.${cloudflare_zone.fluidattacks_com.zone}"
  type     = "TXT"
  value    = "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrLHiExVd55zd/IQ/J/mRwSRMAocV/hMB3jXwaHH36d9NaVynQFYV8NaWi69c1veUtRzGt7yAioXqLj7Z4TeEUoOLgrKsn8YnckGs9i3B3tVFB+Ch/4mPhXWiNfNdynHWBcPcbJ8kjEQ2U8y78dHZj1YeRXXVvWob2OaKynO8/lQIDAQAB;"
  ttl      = 1
  proxied  = false
}

resource "cloudflare_record" "mailgun_smtp" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  name     = "smtp._domainkey.mailgun.${cloudflare_zone.fluidattacks_com.zone}"
  type     = "TXT"
  value    = "k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDWWMDVpf8LmPSxAzXN6maN9tmYF37+LNKt0ClL6xin8F5D6icNdvViPAFuZDUU8aAQPYacWHUPY0ay+95wt2XiGbpZsa7k4EPFYTdL2hfMNwaidDJKgL58kzBcfvR1r/VX3MPmiP0d6cQKqoDi+THtpqd2w270pgCCBKiYvujHmQIDAQAB"
  ttl      = 1
  proxied  = false
}

resource "cloudflare_record" "zoho_verify_dkim" {
  zone_id = cloudflare_zone.fluidattacks_com.id
  name    = "1522905413783._domainkey.${cloudflare_zone.fluidattacks_com.zone}"
  type    = "TXT"
  value   = "k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCr6KMgdxxgg7oT3ulMwPJs9RXgXDrI9UWU118pHEMohl3UbL3Jwp4oxp/9N3thh/3WCJnYV134zbEVolZwqaT3JsFEq/mQ/RpW/JnOZ3rnxqJPurb2bcfJol4SDxiWVObzHX31xnANzFcXnq1/5dMK5QvW4Jh7n0fm4+4ywqiy2QIDAQAB"
  ttl     = 1
  proxied = false
}


# Page Rules

resource "cloudflare_page_rule" "redirect_www" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  target   = "www.${cloudflare_zone.fluidattacks_com.zone}/*"
  status   = "active"
  priority = 2

  actions {
    forwarding_url {
      url         = "https://${cloudflare_zone.fluidattacks_com.zone}/$1"
      status_code = 301
    }
  }
}

resource "cloudflare_page_rule" "install" {
  zone_id  = cloudflare_zone.fluidattacks_com.id
  target   = "${cloudflare_zone.fluidattacks_com.zone}/install"
  status   = "active"
  priority = 1

  actions {
    forwarding_url {
      url         = "https://gitlab.com/fluidattacks/product/-/archive/master/product-master.tar.gz"
      status_code = 301
    }
  }
}
