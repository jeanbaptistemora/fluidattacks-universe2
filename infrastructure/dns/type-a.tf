resource "aws_route53_record" "mainA" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "${aws_route53_zone.fs_maindomain.name}"
  type    = "A"
  alias {
    name    = "${var.elbDns}"
    zone_id = "${var.elbZone}"
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "mail" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "mail.${aws_route53_zone.fs_maindomain.name}"
  type    = "A"
  alias {
    name    = "${var.elbDns}"
    zone_id = "${var.elbZone}"
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "env" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "env.${aws_route53_zone.fs_maindomain.name}"
  type    = "A"
  ttl     = "300"
  records = ["35.192.68.246"]
}

resource "aws_route53_record" "web" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "web.${aws_route53_zone.fs_maindomain.name}"
  type    = "A"
  alias {
    name                   = "s3-website-us-east-1.amazonaws.com."
    zone_id                = "Z3AQBSTGFYJSTF"
    evaluate_target_health = false
  }
}
