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


resource "twilio_verify_services_rate_limits_v2" "phone_number_rate_limit" {
  service_sid = twilio_verify_services_v2.verify.sid
  unique_name = "end_user_phone_number"
}


resource "twilio_verify_services_rate_limits_buckets_v2" "phone_number_rate_limit_bucket" {
  service_sid    = twilio_verify_services_v2.verify.sid
  rate_limit_sid = twilio_verify_services_rate_limits_v2.phone_number_rate_limit.sid
  interval       = 60
  max            = 2
}
