variable "webBucket" {}

module "users" {
  source = "./users"
}

module "providers" {
  source = "./providers"
}

module "groups" {
  source = "./groups"
  fis3integration = "${module.users.fis3integration}"
  examss3 = "${module.users.examss3}"
  fws3user = "${module.users.fws3user}"
}

module "roles" {
  source = "./roles"
  sso = "${module.providers.sso}"
  ssofinance = "${module.providers.ssofinance}"
}

module "policies" {
  source = "./policies"
  webBucket = "${var.webBucket}"
  web = "${module.groups.web}"
  fluidserves = "${module.groups.fluidserves}"
  fis3integration = "${module.groups.fis3integration}"
  ssofinance = "${module.roles.ssofinance}"
}

output "fis3integrationID" {
  value = "${module.users.fis3integrationID}"
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
