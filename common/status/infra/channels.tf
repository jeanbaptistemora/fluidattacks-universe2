# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# Email

resource "checkly_alert_channel" "emails" {
  for_each = {
    for user in var.alertUsers : split("@", user)[0] => user
  }
  email {
    address = each.value
  }

  send_recovery = true
  send_failure  = true
  send_degraded = false

  ssl_expiry           = false
  ssl_expiry_threshold = 1
}

# SMS

resource "checkly_alert_channel" "sms" {
  sms {
    name   = "default"
    number = var.alertSms
  }

  send_recovery = true
  send_failure  = true
  send_degraded = false

  ssl_expiry           = false
  ssl_expiry_threshold = 1
}
