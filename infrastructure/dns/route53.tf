variable "domain" {}
variable "elbDns" {}
variable "elbZone" {}
# AWS vars
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "region" {}
variable "dbInstance" {}

provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region = "${var.region}"
}

resource "aws_route53_zone" "fs_maindomain" {
  name = "${var.domain}"
  comment = "Dominio principal de FLUID"
}
