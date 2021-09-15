resource "cloudflare_rate_limit" "integrates_production" {
  zone_id             = cloudflare_zone.fluidattacks_com.id
  threshold           = 600
  period              = 60
  disabled            = false
  description         = "Integrates production rate limit"
  bypass_url_patterns = []

  match {
    request {
      url_pattern = "app.${cloudflare_zone.fluidattacks_com.zone}/*"
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
