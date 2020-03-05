variable "fsBucket" {}
variable "region" {}

resource "aws_iam_account_password_policy" "strict" {
  allow_users_to_change_password = true
  hard_expiry                    = false
  max_password_age               = 30
  minimum_password_length        = 14
  password_reuse_prevention      = 24
  require_lowercase_characters   = true
  require_numbers                = true
  require_symbols                = true
  require_uppercase_characters   = true
}

module "policies" {
  source             = "./policies"
  fsBucket           = var.fsBucket
}
