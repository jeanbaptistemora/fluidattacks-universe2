
module "groups" {
  source = "./groups"
}

module "roles" {
  source = "./roles"
}

module "policies" {
  source = "./policies"
  web = "${module.groups.web}"
  lambdacallers = "${module.groups.lambdacallers}"
  fluidserves = "${module.groups.fluidserves}"
  fis3integration = "${module.groups.fis3integration}"
  ssofinance = "${module.roles.ssofinance}"
}
