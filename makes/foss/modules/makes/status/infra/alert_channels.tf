# Email

resource "checkly_alert_channel" "emails" {
  for_each = {
    for user in var.alertChannelUsers : split("@", user)[0] => user
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

resource "checkly_alert_channel" "default" {
  sms {
    name   = "default"
    number = "+573207881879"
  }

  send_recovery = true
  send_failure  = true
  send_degraded = false

  ssl_expiry           = false
  ssl_expiry_threshold = 1
}
