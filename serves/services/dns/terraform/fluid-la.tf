locals {
  fluidLaIndex = index(var.secDomains, "fluid.la")
}

# MX Records
resource "aws_route53_record" "fluidLaMX" {
  zone_id = aws_route53_zone.fs_old_domains[local.fluidLaIndex].zone_id
  name    = "fluid.la"
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

