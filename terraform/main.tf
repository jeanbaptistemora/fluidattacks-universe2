
provider "aws" {
  access_key = "${var.acc_key}"
  secret_key = "${var.sec_key}"
  region = "${var.reg}"
}

module "createNetwork" {
  source = "./network"
  sreg = "${var.sreg}"
  cdir = "${var.cdir}"
}

module "ec2instance" {
  source = "./ec2"
  amiID = "${var.amiID}"
  iType = "${var.iType}"
  sgId = "${module.createNetwork.sgId}"
  snetId = "${module.createNetwork.snetId}"
  kName = "${var.kName}"
}

# module "r53" {
#   source = "./dns"
#   server = "${module.ec2instance.ip}"
# }
#
# module "iam" {
#   source = "./iam"
# }

output "instance_ip" {
  value = "${module.ec2instance.ip}"
}
