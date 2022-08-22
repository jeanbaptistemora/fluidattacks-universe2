resource "cloudflare_rate_limit" "integrates_production" {
  zone_id             = cloudflare_zone.fluidattacks_com.id
  threshold           = 200
  period              = 60
  disabled            = false
  description         = "Integrates production"
  bypass_url_patterns = []

  match {
    request {
      url_pattern = "app.${cloudflare_zone.fluidattacks_com.zone}/*"
      schemes     = ["_ALL_"]
      methods     = ["_ALL_"]
    }
    response {
      origin_traffic = true

      headers = [
        {
          "name"  = "Cf-Cache-Status"
          "op"    = "ne"
          "value" = "HIT"
        },
      ]
    }
  }

  action {
    mode    = "ban"
    timeout = 60
  }

  correlate {
    by = "nat"
  }
}
