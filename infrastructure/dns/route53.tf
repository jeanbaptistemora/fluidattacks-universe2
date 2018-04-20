variable "server" {}
variable "domain" {}
# AWS vars
variable "acc_key" {}
variable "sec_key" {}
variable "reg" {}

provider "aws" {
  access_key = "${var.acc_key}"
  secret_key = "${var.sec_key}"
  region = "${var.reg}"
}

resource "aws_route53_zone" "fs_maindomain" {
  name = "${var.domain}"
  comment = "Dominio principal de FLUID"
}
