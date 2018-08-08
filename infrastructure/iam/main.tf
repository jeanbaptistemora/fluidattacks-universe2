variable "fwBucket" {}

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

module "users" {
  source = "./users"
}

module "providers" {
  source = "./providers"
}

module "groups" {
  source = "./groups"
  fiDynamo        = "${module.users.fiDynamo}"
  fis3integration = "${module.users.fis3integration}"
  examss3         = "${module.users.examss3}"
  fws3user        = "${module.users.fws3user}"
}

module "roles" {
  source = "./roles"
  sso = "${module.providers.sso}"
  ssofinance = "${module.providers.ssofinance}"
}

module "policies" {
  source = "./policies"
  fwBucket = "${var.fwBucket}"
  web = "${module.groups.web}"
  fluidserves = "${module.groups.fluidserves}"
  fis3integration = "${module.groups.fis3integration}"
  fiDynamo = "${module.groups.fiDynamo}"
  ssofinance = "${module.roles.ssofinance}"
}

output "fis3integrationID" {
  value = "${module.users.fis3integrationID}"
}

output "fiS3Arn" {
  value = "${module.users.fiS3Arn}"
}

output "cloudwatchID" {
  value = "${module.users.cloudwatchID}"
}

output "fluidintegratesdynamoID" {
  value = "${module.users.fluidintegratesdynamoID}"
}

output "fws3userID" {
  value = "${module.users.fws3userID}"
}

#
output "fis3integrationSECRET" {
  value = "${module.users.fis3integrationSECRET}"
}

output "cloudwatchSECRET" {
  value = "${module.users.cloudwatchSECRET}"
}

output "fluidintegratesdynamoSECRET" {
  value = "${module.users.fluidintegratesdynamoSECRET}"
}

output "fws3userSECRET" {
  value = "${module.users.fws3userSECRET}"
}
