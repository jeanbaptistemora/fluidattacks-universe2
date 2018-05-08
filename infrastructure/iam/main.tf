variable "webBucket" {}
variable "mainZoneID" {}

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
  fir53review = "${module.users.fir53review}"
  mainZoneID = "${var.mainZoneID}"
  ssofinance = "${module.roles.ssofinance}"
}
