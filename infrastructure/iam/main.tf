
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
  web = "${module.groups.web}"
  lambdacallers = "${module.groups.lambdacallers}"
  fluidserves = "${module.groups.fluidserves}"
  fis3integration = "${module.groups.fis3integration}"
  ssofinance = "${module.roles.ssofinance}"
}
