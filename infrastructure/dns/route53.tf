variable "server" {}

variable "domain" {}

resource "aws_route53_zone" "fs_maindomain" {
  name = "${var.domain}"
  comment = "Dominio principal de FLUID"
}
