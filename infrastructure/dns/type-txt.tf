
resource "aws_route53_record" "mainTXT" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["v=spf1 include:spf.mandrillapp.com ?all",
            "v=spf1 include:servers.mcsv.net ?all",
            "google-site-verification=SK6CMgAtuuw7tR6eCev6XY8D6rjn9BW8AGd5KWS1b5g",
            "MS=ms97836067"]
}

resource "aws_route53_record" "mailgunTXT" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "mailgun.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["v=spf1 include:mailgun.org ~all"]
}

resource "aws_route53_record" "mandrill_domainkey" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "mandrill._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrLHiExVd55zd/IQ/J/mRwSRMAocV/hMB3jXwaHH36d9NaVynQFYV8NaWi69c1veUtRzGt7yAioXqLj7Z4TeEUoOLgrKsn8YnckGs9i3B3tVFB+Ch/4mPhXWiNfNdynHWBcPcbJ8kjEQ2U8y78dHZj1YeRXXVvWob2OaKynO8/lQIDAQAB;"]
}

resource "aws_route53_record" "smtp_domainkey" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "smtp._domainkey.mailgun.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDWWMDVpf8LmPSxAzXN6maN9tmYF37+LNKt0ClL6xin8F5D6icNdvViPAFuZDUU8aAQPYacWHUPY0ay+95wt2XiGbpZsa7k4EPFYTdL2hfMNwaidDJKgL58kzBcfvR1r/VX3MPmiP0d6cQKqoDi+THtpqd2w270pgCCBKiYvujHmQIDAQAB"]
}
