terraform {
  required_providers {
    twilio = {
      source  = "twilio/twilio"
      version = ">=0.4.0"
    }
  }
}

resource "twilio_verify_services_v2" "verify" {
  friendly_name         = "asm verification service"
  code_length           = 6
  lookup_enabled        = true
  skip_sms_to_landlines = true
}
