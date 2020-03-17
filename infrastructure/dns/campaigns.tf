resource "aws_route53_record" "usa" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "usa.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["60afa14d825c49689b84f58f10773196.unbouncepages.com"]
}

resource "aws_route53_record" "mx" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "mx.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["24f071411dac41ee92f1696a216452ce.unbouncepages.com"]
}

resource "aws_route53_record" "co" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "co.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["a225c559a539440da8db95028eefe647.unbouncepages.com"]
}

resource "aws_route53_record" "cl" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "cl.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["ef05e236be914278848022ff8d6c69aa.unbouncepages.com"]
}

resource "aws_route53_record" "ec" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "ec.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["21d7fc60279245bd8ddc9c30fdc7c4d4.unbouncepages.com"]
}

resource "aws_route53_record" "pe" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "pe.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["4b16a2950ab4429f9bbcea4e5beb94e5.unbouncepages.com"]
}

resource "aws_route53_record" "gt" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "gt.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["f411f94104a84e749859d2aa58c9180a.unbouncepages.com"]
}

resource "aws_route53_record" "pa" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "pa.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["a527a846db874c8498ed6540b2c68962.unbouncepages.com"]
}

resource "aws_route53_record" "report2020" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "report2020.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["64b61b566e6b494db43ea4242748637a.unbouncepages.com"]
}

resource "aws_route53_record" "thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "thanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["fec04f69a10c416ca5f5bdee29348819.unbouncepages.com"]
}
