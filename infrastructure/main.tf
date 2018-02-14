
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
  start_all = "${var.start_all}"
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

# existing R53
module "existing-r53" {
  source = "./existing-dns"
  server = "${module.ec2instance.ip}"
  zone = "${var.hzoneID}"
  domain = "${var.zoneName}"
 }

output "instance_ip" {
  value = "${module.ec2instance.ip}"
}
