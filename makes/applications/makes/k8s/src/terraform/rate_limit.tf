resource "cloudflare_rate_limit" "integrates_production" {
  zone_id             = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  threshold           = 600
  period              = 60
  disabled            = false
  description         = "Integrates production rate limit"
  bypass_url_patterns = []

  match {
    request {
      url_pattern = "integrates.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
      schemes     = ["_ALL_"]
      methods     = ["_ALL_"]
    }
    response {
      origin_traffic = true
    }
  }

  action {
    mode = "js_challenge"
  }

  correlate {
    by = "nat"
  }
}
