resource "aws_route53_record" "usa" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "usa.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["60afa14d825c49689b84f58f10773196.unbouncepages.com"]
}

resource "aws_route53_record" "thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "thanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["fec04f69a10c416ca5f5bdee29348819.unbouncepages.com"]
}

resource "aws_route53_record" "mx" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "mx.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["24f071411dac41ee92f1696a216452ce.unbouncepages.com"]
}

resource "aws_route53_record" "mx-thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "mxthanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["448937d80e93489092c29be14fa9d910.unbouncepages.com"]
}

resource "aws_route53_record" "co" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "co.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["a225c559a539440da8db95028eefe647.unbouncepages.com"]
}

resource "aws_route53_record" "co-thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "cothanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["2fd0ffc273264ea8ba71af40b1a88d5e.unbouncepages.com"]
}

resource "aws_route53_record" "cl" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "cl.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["ef05e236be914278848022ff8d6c69aa.unbouncepages.com"]
}

resource "aws_route53_record" "cl-thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "clthanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["2ccbfd25c559470b85d7efa6c2983fc2.unbouncepages.com"]
}

resource "aws_route53_record" "ec" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "ec.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["21d7fc60279245bd8ddc9c30fdc7c4d4.unbouncepages.com"]
}

resource "aws_route53_record" "ec-thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "ecthanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["04b8415555b9428aa0963090629150d7.unbouncepages.com"]
}

resource "aws_route53_record" "pe" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "pe.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["4b16a2950ab4429f9bbcea4e5beb94e5.unbouncepages.com"]
}

resource "aws_route53_record" "pe-thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "pethanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["3350131285cb450b8ebad927720f611f.unbouncepages.com"]
}

resource "aws_route53_record" "gt" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "gt.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["f411f94104a84e749859d2aa58c9180a.unbouncepages.com"]
}

resource "aws_route53_record" "gt-thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "gtthanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["6a32005e6172404e8faa6aa8e08cc172.unbouncepages.com"]
}

resource "aws_route53_record" "pa" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "pa.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["a527a846db874c8498ed6540b2c68962.unbouncepages.com"]
}

resource "aws_route53_record" "pa-thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "pathanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["72e8a0f8c5d24e988b5acbc4efe12b0a.unbouncepages.com"]
}

resource "aws_route53_record" "cr" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "cr.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["548b68155f34459b874184ec50b4cb7d.unbouncepages.com"]
}

resource "aws_route53_record" "cr-thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "crthanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["6f08d2c5b09f490ebf4dc38521c7d8f3.unbouncepages.com"]
}

resource "aws_route53_record" "rd" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "rd.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["5be885e667b7458e902416402b56bff2.unbouncepages.com"]
}

resource "aws_route53_record" "rd-thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "rdthanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["08ec73f964f04ff8a051d741f659619e.unbouncepages.com"]
}

resource "aws_route53_record" "report2020" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "report2020.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["64b61b566e6b494db43ea4242748637a.unbouncepages.com"]
}
