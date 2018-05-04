resource "aws_route53_record" "6002333" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "6002333.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["sendgrid.net"]
}

resource "aws_route53_record" "env_cname" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "*.env.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["env.fluidattacks.com"]
}

resource "aws_route53_record" "emailmkt" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "emailmkt.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "3600"
  records = ["u6002333.wl084.sendgrid.net"]
}


resource "aws_route53_record" "go_fluid" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "go.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["rebrandlydomain.com"]
}

resource "aws_route53_record" "k1_domainkey" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "k1._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["dkim.mcsv.net"]
}

resource "aws_route53_record" "kb_fluid" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "kb.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["fluid.knowledgeowl.com"]
}

resource "aws_route53_record" "landing" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "landing.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "3600"
  records = ["pages.rdstation.com.br"]
}

resource "aws_route53_record" "mailguntracking" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "mailguntracking.mailgun.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["mailgun.org"]
}

resource "aws_route53_record" "marketing_fluid" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "marketing.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["u6002333.wl084.sendgrid.net"]
}

resource "aws_route53_record" "s1_domainkey" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "s1._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "3600"
  records = ["s1.domainkey.u6002333.wl084.sendgrid.net"]
}

resource "aws_route53_record" "s2_domainkey" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "s2._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "3600"
  records = ["s2.domainkey.u6002333.wl084.sendgrid.net"]
}

resource "aws_route53_record" "servicios_fluid" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "servicios.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "3600"
  records = ["pages.rdstation.com.br"]
}

resource "aws_route53_record" "status_fluid" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "status.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["stats.pingdom.com"]
}

resource "aws_route53_record" "t_emailmkt" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "t.emailmkt.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "3600"
  records = ["sendgrid.net"]
}

resource "aws_route53_record" "t_marketing" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "t.marketing.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["sendgrid.net"]
}

resource "aws_route53_record" "track" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "track.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["mandrillapp.com"]
}

resource "aws_route53_record" "www" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "www.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["fluidattacks.com"]
}


resource "aws_route53_record" "database" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "database.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["${var.db_instance}"]
}

resource "aws_route53_record" "main_to_bucket" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "main.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["web.fluidattacks.com"]
}
