variable "acc_key" {}
variable "sec_key" {}
variable "reg" {}

provider "aws" {
  access_key = "${var.acc_key}"
  secret_key = "${var.sec_key}"
  region = "${var.reg}"
}

module "ec2instance" {
  source = "./ec2"
}
