# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "cloudflare_rate_limit" "integrates_production_api" {
  zone_id             = cloudflare_zone.fluidattacks_com.id
  threshold           = 200
  period              = 60
  disabled            = false
  description         = "Integrates production API"
  bypass_url_patterns = []

  match {
    request {
      url_pattern = "app.${cloudflare_zone.fluidattacks_com.zone}/api"
      schemes     = ["_ALL_"]
      methods     = ["POST"]
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
