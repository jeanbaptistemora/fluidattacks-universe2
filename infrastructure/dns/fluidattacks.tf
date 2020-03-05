# A Records
resource "aws_route53_record" "web" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "web.${aws_route53_zone.fs_maindomain.name}"
  type    = "A"
  alias {
    name                   = "s3-website-us-east-1.amazonaws.com."
    zone_id                = var.s3-east-1-zone-id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "web-ephemeral" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "web.eph.${aws_route53_zone.fs_maindomain.name}"
  type    = "A"
  alias {
    name                   = "s3-website-us-east-1.amazonaws.com."
    zone_id                = var.s3-east-1-zone-id
    evaluate_target_health = false
  }
}

# CNAME records
resource "aws_route53_record" "thanks" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "thanks.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["fec04f69a10c416ca5f5bdee29348819.unbouncepages.com"]
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

resource "aws_route53_record" "mail" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "mail.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["ghs.googlehosted.com"]
}

resource "aws_route53_record" "sendgrid" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "6002333.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["sendgrid.net"]
}

resource "aws_route53_record" "env_cname" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "*.env.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["fluidattacks.com"]
}

resource "aws_route53_record" "emailmkt" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "emailmkt.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "3600"
  records = ["u6002333.wl084.sendgrid.net"]
}

resource "aws_route53_record" "go_fluid" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "go.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["rebrandlydomain.com"]
}

resource "aws_route53_record" "k1_domainkey" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "k1._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["dkim.mcsv.net"]
}

resource "aws_route53_record" "kb_fluid" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "kb.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["fluid.knowledgeowl.com"]
}

resource "aws_route53_record" "mailguntracking" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "mailguntracking.mailgun.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["mailgun.org"]
}

resource "aws_route53_record" "marketing_fluid" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "marketing.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["u6002333.wl084.sendgrid.net"]
}

resource "aws_route53_record" "s1_domainkey" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "s1._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "3600"
  records = ["s1.domainkey.u6002333.wl084.sendgrid.net"]
}

resource "aws_route53_record" "s2_domainkey" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "s2._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "3600"
  records = ["s2.domainkey.u6002333.wl084.sendgrid.net"]
}

resource "aws_route53_record" "status_fluid" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "status.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["stats.pingdom.com"]
}

resource "aws_route53_record" "t_emailmkt" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "t.emailmkt.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "3600"
  records = ["sendgrid.net"]
}

resource "aws_route53_record" "t_marketing" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "t.marketing.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["sendgrid.net"]
}

resource "aws_route53_record" "track" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "track.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["mandrillapp.com"]
}

resource "aws_route53_record" "www" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "www.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["fluidattacks.com"]
}

resource "aws_route53_record" "customerio" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "customerio.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["e.customeriomail.com"]
}

resource "aws_route53_record" "discourse" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "community.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["fluidattacks.hosted-by-discourse.com"]
}

resource "aws_route53_record" "mattermost" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "chat.${aws_route53_zone.fs_maindomain.name}"
  type    = "CNAME"
  ttl     = "300"
  records = ["fluidattacks.com"]
}

# MX Records
resource "aws_route53_record" "mainMX" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = aws_route53_zone.fs_maindomain.name
  type    = "MX"
  ttl     = "300"
  records = [
    "5 ALT1.ASPMX.L.GOOGLE.COM.",
    "1 ASPMX.L.GOOGLE.COM.",
    "5 ALT2.ASPMX.L.GOOGLE.COM.",
    "10 ASPMX2.GOOGLEMAIL.COM.",
    "10 ASPMX3.GOOGLEMAIL.COM.",
  ]
}

resource "aws_route53_record" "mailgunMX" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "mailgun.${aws_route53_zone.fs_maindomain.name}"
  type    = "MX"
  ttl     = "300"
  records = ["10 mxb.mailgun.org", "10 mxa.mailgun.org"]
}

# TXT Records
resource "aws_route53_record" "mainTXT" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = aws_route53_zone.fs_maindomain.name
  type    = "TXT"
  ttl     = "300"
  records = [
    "v=spf1 include:_spf.google.com include:spf.mandrillapp.com include:servers.mcsv.net include:customeriomail.com include:_spf.salesforce.com -all",
    "google-site-verification=SK6CMgAtuuw7tR6eCev6XY8D6rjn9BW8AGd5KWS1b5g",
    "google-site-verification=zVcDOWOKonibpIrLLyFEuy8jbpTJyOPiA39vngIpEvI",
    "MS=ms97836067",
  ]
}

resource "aws_route53_record" "email_dmarc" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "_dmarc.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["v=DMARC1; p=none; rua=mailto:technology+dmarc@fluidattacks.com"]
}

resource "aws_route53_record" "googleTXT" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "google._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoVfDxzz1BbwFFyeQvKe7B4YMSR1HWmjCu4PQzESyAAc9XQDSbtoYQNCHaHisTJNgh4OGEWvgRcpsVljffC5jO3tHcra8xW8ls5O16sClQtfitcKhC1VxNbqYoAnUSNv9FBcsldK96jQgeMrsZUMo6SdldCDO\"\"kX7vOjgLzDw6dOMAENSoU3NsMfRwoDaanCf2gkFb+5mOtDUZCHukM5rpj+ePc3GJAzX8bakMdWD7BlZnPT0fRVcSQGOAM1GVcSDYR465hdBkADJg3KM2TdPTC/XLwEQXgqRZXVWMtSu/Rb/DcHILZNmzKxUk/B4eKjXGQDbs9hshgsqsZGYEbhOvrwIDAQAB"]
}

resource "aws_route53_record" "salesforceDKIM" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "salesforce.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqiBCWoHf5vbibfUS9UO1WiPXA1ZuUqR+yQdbbZLacQuQBB5HuCfylr4soetxurxTg4a7KN6EcDexy/4nGaxxdmDWrYx9bKP1AtNtTL4pwkkI3c1H9jWJTRyqRPTLg+c5qqzNBNYaGcOVEXWUruOvuwO39w3A\"\"NIiOdt6grMh+vM7p1Kr/M8bITcQz92Yx0kWN9DZPcXf++v5jlP39VCAd0QOPZIVGBWvNAkD1gGvDl2fe3YCGSXkEt7F8WD/K1RhUBGI/+3GamRGX2K6c0wVpdmzUPF447VRSO1PQzhOP6JMZAoiY7tssZVW5JiBesTlbLsKWK9Vrry+mayLOexdysQIDAQAB"]
}

resource "aws_route53_record" "mandrill_domainkey" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "mandrill._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrLHiExVd55zd/IQ/J/mRwSRMAocV/hMB3jXwaHH36d9NaVynQFYV8NaWi69c1veUtRzGt7yAioXqLj7Z4TeEUoOLgrKsn8YnckGs9i3B3tVFB+Ch/4mPhXWiNfNdynHWBcPcbJ8kjEQ2U8y78dHZj1YeRXXVvWob2OaKynO8/lQIDAQAB;"]
}

resource "aws_route53_record" "smtp_domainkey" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "smtp._domainkey.mailgun.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDWWMDVpf8LmPSxAzXN6maN9tmYF37+LNKt0ClL6xin8F5D6icNdvViPAFuZDUU8aAQPYacWHUPY0ay+95wt2XiGbpZsa7k4EPFYTdL2hfMNwaidDJKgL58kzBcfvR1r/VX3MPmiP0d6cQKqoDi+THtpqd2w270pgCCBKiYvujHmQIDAQAB"]
}

resource "aws_route53_record" "customerio_ownership" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "46393._cio.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["c4ae35cc23959de2ef5f0d9e036c2cc23ec79777"]
}

resource "aws_route53_record" "customerio_dkim" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = "smtpapi._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["k=rsa; t=s; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDPtW5iwpXVPiH5FzJ7Nrl8USzuY9zqqzjE0D1r04xDN6qwziDnmgcFNNfMewVKN2D1O+2J9N14hRprzByFwfQW76yojh54Xu3uSbQ3JP0A7k8o8GutRF8zbFUA8n0ZH2y0cIEjMliXY4W4LwPA7m4q0ObmvSjhd63O9d8z1XkUBwIDAQAB"]
}
