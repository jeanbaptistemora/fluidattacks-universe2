# AWS vars
variable "acc_key" {}
variable "sec_key" {}
variable "reg" {}
variable "sreg" {}

#EC2 vars
variable "amiID" {}
variable "iType" {}
variable "kName" {}

# Net Vars
variable "cdir" {}

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

output "instance_ip" {
  value = "${module.ec2instance.ip}"
}
