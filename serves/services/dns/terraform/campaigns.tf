resource "aws_route53_record" "landing" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "landing.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["a2cbfad5d1d14c9eb6099182bb1adb48.unbouncepages.com"]
}

resource "aws_route53_record" "usa" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "usa.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["60afa14d825c49689b84f58f10773196.unbouncepages.com"]
}

resource "aws_route53_record" "report2020" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "report2020.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["64b61b566e6b494db43ea4242748637a.unbouncepages.com"]
}
