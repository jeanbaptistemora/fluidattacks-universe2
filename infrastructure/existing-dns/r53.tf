variable "zone" {}
variable "server" {}
variable "domain" {}

variable "domain2" {}
variable "zone2" {}

# AWS vars
variable "acc_key" {}
variable "sec_key" {}
variable "reg" {}

provider "aws" {
  access_key = "${var.acc_key}"
  secret_key = "${var.sec_key}"
  region = "${var.reg}"
}

# fluidattacks
resource "aws_route53_record" "main" {
  zone_id = "${var.zone}"
  name    = "${var.domain}"
  type    = "A"
  ttl     = "300"
  records = ["${var.server}"]
}

resource "aws_route53_record" "mail" {
  zone_id = "${var.zone}"
  name    = "mail.${var.domain}"
  type    = "A"
  ttl     = "300"
  records = ["${var.server}"]
}

# fluidla
resource "aws_route53_record" "main2" {
  zone_id = "${var.zone2}"
  name    = "${var.domain2}"
  type    = "A"
  ttl     = "300"
  records = ["${var.server}"]
}

resource "aws_route53_record" "mail2" {
  zone_id = "${var.zone2}"
  name    = "mail.${var.domain2}"
  type    = "A"
  ttl     = "300"
  records = ["${var.server}"]
}
