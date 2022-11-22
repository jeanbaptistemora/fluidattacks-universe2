# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "okta_org_configuration" "main" {
  company_name              = "Fluid Attacks"
  website                   = "https://fluidattacks.com/"
  end_user_support_help_url = "https://help.fluidattacks.tech/"

  address_1   = "95 3rd St"
  city        = "San Francisco"
  state       = "California"
  country     = "United States of America"
  postal_code = "94103"

  billing_contact_user   = okta_user.users["mparra"].id
  technical_contact_user = okta_user.users["fmoreno"].id
}

resource "okta_policy_password_default" "main" {
  password_min_length    = 16
  password_min_lowercase = 1
  password_min_uppercase = 1
  password_min_number    = 1
  password_min_symbol    = 1

  password_max_age_days         = 30
  password_expire_warn_days     = 5
  password_min_age_minutes      = 120
  password_history_count        = 24
  password_max_lockout_attempts = 10
  password_auto_unlock_minutes  = 10

  password_exclude_username   = true
  password_exclude_first_name = true
  password_exclude_last_name  = true
  password_dictionary_lookup  = true

  email_recovery    = "ACTIVE"
  question_recovery = "ACTIVE"
  sms_recovery      = "INACTIVE"
  call_recovery     = "INACTIVE"

  password_show_lockout_failures         = true
  password_lockout_notification_channels = ["EMAIL"]

  recovery_email_token = 60
}

resource "okta_factor" "okta_otp" {
  provider_id = "okta_otp"
  active      = true
}

resource "okta_factor" "okta_push" {
  provider_id = "okta_push"
  active      = true
}

resource "okta_policy_mfa_default" "main" {
  okta_otp = {
    enroll = "REQUIRED"
  }

  okta_push = {
    enroll = "OPTIONAL"
  }

  depends_on = [
    okta_factor.okta_otp,
    okta_factor.okta_push,
  ]
}

resource "okta_policy_signon" "main" {
  name            = "main"
  status          = "ACTIVE"
  groups_included = [data.okta_group.everyone.id]
}

resource "okta_policy_rule_signon" "main" {
  policy_id          = okta_policy_signon.main.id
  name               = "main"
  access             = "ALLOW"
  network_connection = "ANYWHERE"
  status             = "ACTIVE"
  risc_level         = ""

  mfa_required = true
  mfa_prompt   = "SESSION"
  mfa_lifetime = 1440

  session_idle       = 10080
  session_lifetime   = 10080
  session_persistent = false
}
