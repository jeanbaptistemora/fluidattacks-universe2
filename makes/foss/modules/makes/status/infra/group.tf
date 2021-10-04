resource "checkly_check_group" "fluidattacks" {
  name         = "Fluid Attacks test"
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
    BITBUCKET_PWD        = var.bitbucketPwd
    BITBUCKET_USER       = var.bitbucketUser
    CHECKLY_API_KEY      = var.checklyApiKey
    INTEGRATES_API_TOKEN = var.integratesApiToken
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
}
