resource "aws_route53_record" "mainMX" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "${aws_route53_zone.fs_maindomain.name}"
  type    = "MX"
  ttl     = "300"
  records = ["5 ALT1.ASPMX.L.GOOGLE.COM.","1 ASPMX.L.GOOGLE.COM.",
             "5 ALT2.ASPMX.L.GOOGLE.COM.","10 ASPMX2.GOOGLEMAIL.COM.",
             "10 ASPMX3.GOOGLEMAIL.COM."]
}

resource "aws_route53_record" "mailgunMX" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "mailgun.${aws_route53_zone.fs_maindomain.name}"
  type    = "MX"
  ttl     = "300"
  records = ["10 mxb.mailgun.org","10 mxa.mailgun.org"]
}
