# Page Rules

resource "cloudflare_page_rule" "main_to_fluidattacks_com" {
  zone_id  = cloudflare_zone.main.id
  target   = "https://${cloudflare_zone.main.zone}/*"
  status   = "active"
  priority = 1

  actions {
    forwarding_url {
      url         = "https://fluidattacks.com/$1"
      status_code = 301
    }
  }
}

resource "cloudflare_page_rule" "www_main_to_main" {
  zone_id  = cloudflare_zone.main.id
  target   = "https://www.${cloudflare_zone.main.zone}/*"
  status   = "active"
  priority = 2

  actions {
    forwarding_url {
      url         = "https://${cloudflare_zone.main.zone}/$1"
      status_code = 301
    }
  }
}
