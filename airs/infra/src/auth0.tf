# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "auth0_attack_protection" "airs_protection" {
  suspicious_ip_throttling {
    enabled   = true
    shields   = ["admin_notification", "block"]
    allowlist = []

    pre_login {
      max_attempts = 100
      rate         = 864000
    }

    pre_user_registration {
      max_attempts = 50
      rate         = 1200
    }
  }

  brute_force_protection {
    allowlist    = []
    enabled      = true
    max_attempts = 5
    mode         = "count_per_identifier_and_ip"
    shields      = ["block", "user_notification"]
  }

  breached_password_detection {
    admin_notification_frequency = ["immediately"]
    enabled                      = true
    method                       = "standard"
    shields                      = ["admin_notification", "block"]
  }
}

resource "auth0_branding" "fluid_attacks_airs" {
  logo_url = "https://res.cloudinary.com/fluid-attacks/image/upload/q_auto,f_auto/v1622583388/airs/logo_fluid_attacks_2021_eqop3k.svg"
}

resource "auth0_client" "fluid_attacks_airs" {
  name                       = "Airs"
  description                = "Fluid Attacks main Website"
  app_type                   = "spa"
  token_endpoint_auth_method = "none"
  callbacks                  = ["https://fluidattacks.com/"]
  allowed_origins            = ["https://fluidattacks.com/"]
  allowed_logout_urls        = ["https://fluidattacks.com/"]
  web_origins                = ["https://fluidattacks.com/"]
  grant_types = [
    "authorization_code",
    "implicit",
    "refresh_token"
  ]

  refresh_token {
    idle_token_lifetime = 21600
    leeway              = 0
    token_lifetime      = 3600
    rotation_type       = "rotating"
    expiration_type     = "expiring"
  }
}
