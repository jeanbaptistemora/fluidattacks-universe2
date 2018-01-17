
resource "aws_route53_record" "mainTXT" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  records = ["v=spf1 include:_spf.google.com include:servers.mcsv.net include:amazonses.com -all",
              "detectify-verification=4440a65abc64252b0152a9b3c84a1556"]
}

resource "aws_route53_record" "google_domainkey" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "google._domainkey.${aws_route53_zone.fs_maindomain.name}"
  type    = "TXT"
  ttl     = "300"
  # Record too big, need to put \"\" between it
  records = ["v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx+xoz9Br2pk6tPeDrPV/uj7SdMNw9JpxurqL6w1o2f24S4X+QBSR/JaVKoh2FnFj56b9U4R4vWD4aeYk/U5Mwm6AyeXFw/yMG1H",
            "wkHDRAna2/gII69ZcH2M+oSCWZwf0IkYT6oyZch7mpFDy5sU26cWWhi+p10mslmpp02eQbMs2fTM9WxlfOiA4kD9BujFSafhW/yHcUpXVQKoVp+C26ZvmM7hNvK++HoWLxOFtVoxje6zfiE86G1SbXKCuufmcJnjva8\"\"K2nYW07qYZAgftBGXJUZTYLYkrMWYK4q4ghcsgJY9zBQpZmFfRcTvoLhZso8SZmt6Q7Rcvs/8isuzb7wIDAQAB"]
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
  records = ["k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCxsYPafpwBbdM5iBGzUnFuH6m+wMfrROZtqA3inNwvYRPqFjSNktG7d29ubw4xqCogVhEC4BKLzZ704rjfY3xeIjVQj7qRFPW8D4YSaOr/ZiHg9ewD9gp6cZr/uNi2seKMzdCzIbyQ6LMN9XnN7qztIh3mRZXcfTjnnu/Saw1XzwIDAQAB"]
}
