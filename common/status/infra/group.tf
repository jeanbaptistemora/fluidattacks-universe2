# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "checkly_check_group" "fluidattacks" {
  name         = "Fluid Attacks"
  activated    = true
  muted        = false
  concurrency  = 3
  double_check = true

  tags = ["production"]

  locations = [
    "us-east-1",
    "sa-east-1",
    "eu-central-1",
    "ap-east-1",
  ]

  environment_variables = {
    BITBUCKET_PWD        = var.envBitBucketPwd
    BITBUCKET_USER       = var.envBitBucketUser
    CHECKLY_API_KEY      = var.apiKey
    INTEGRATES_API_TOKEN = var.envIntegratesApiToken
  }

  use_global_alert_settings = false
  alert_settings {
    escalation_type = "RUN_BASED"

    run_based_escalation {
      failed_run_threshold = 2
    }

    reminders {
      amount   = 1
      interval = 10
    }

    ssl_certificates {
      enabled         = false
      alert_threshold = 3
    }

    time_based_escalation {
      minutes_failing_threshold = 5
    }
  }

  dynamic "alert_channel_subscription" {
    for_each = {
      for user in var.alertUsers : split("@", user)[0] => user
    }
    content {
      channel_id = checkly_alert_channel.emails[alert_channel_subscription.key].id
      activated  = true
    }
  }
  alert_channel_subscription {
    channel_id = checkly_alert_channel.sms.id
    activated  = true
  }
}
