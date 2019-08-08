variable "fsBucket" {}
variable "fwBucket" {}
variable "region" {}
variable "asserts-bucket" {}
variable "asserts_projects" {
  type = "map"
}

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

module "providers" {
  source = "./providers"
}

module "users" {
  source = "./users"
  asserts-bucket = "${var.asserts-bucket}"
  asserts_projects = "${var.asserts_projects}"
}

module "roles" {
  source = "./roles"
  sso = "${module.providers.sso}"
  ssofinance = "${module.providers.ssofinance}"
}

module "policies" {
  source       = "./policies"
  fsBucket     = "${var.fsBucket}"
  fwBucket     = "${var.fwBucket}"
  ssofinance   = "${module.roles.ssofinance}"
  asserts-bucket = "${var.asserts-bucket}"
}
