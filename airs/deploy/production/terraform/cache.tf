resource "cloudflare_page_rule" "cache" {
  zone_id  = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  target   = "${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  status   = "active"

  actions {
    cache_level            = "cache_everything"
    edge_cache_ttl         = 1800
    browser_cache_ttl      = 1800
    bypass_cache_on_cookie = "CookieConsent"
  }
}
