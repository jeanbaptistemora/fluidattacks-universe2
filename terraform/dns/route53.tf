variable "server" {}

variable "domain" {
    default="fluid.la."
}

resource "aws_route53_zone" "fs_maindomain" {
  name = "${var.domain}"
  comment = "Dominio principal de FLUID"
}
