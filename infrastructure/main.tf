
provider "aws" {
  access_key = "${var.acc_key}"
  secret_key = "${var.sec_key}"
  region = "${var.reg}"
}

# Create from scratch
module "createNetwork" {
  source = "./network"
  sreg = "${var.sreg}"
  cdir = "${var.cdir}"
  ciIP = "${var.ciIP}"
}

# Create from scratch
module "ec2instance" {
  source = "./ec2"
  amiID = "${var.amiID}"
  iType = "${var.iType}"
  sgId = "${module.createNetwork.sgId}"
  snetId = "${module.createNetwork.snetId}"
  kName = "${var.kName}"

  docker = "${var.docker}"

}

# Create from scratch
# module "r53" {
#   source = "./dns"
#   server = "${module.ec2instance.ip}"
#   domain = "${var.zoneName}"
# }

# Create from scratch
# module "iam" {
#   source = "./iam"
# }

output "variable_ip" {
  value = "server=\"${module.ec2instance.ip}\""
}

output "instance_ip" {
  value = "${module.ec2instance.ip}"
}
