variable "zone" {}
variable "server" {}
variable "domain" {}

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
