variable "old_domains" {
  type = "list"
}

resource "aws_route53_zone" "fs_old_domains" {
  count   = 2
  name    = "${element(var.old_domains, count.index)}" 
  comment = "Dominio secundario de Fluid Attacks"
  force_destroy = true
}

resource "aws_route53_record" "old_domains_elb" {
  count   = 2
  zone_id = "${aws_route53_zone.fs_old_domains.*.zone_id[count.index]}"
  name    = "${aws_route53_zone.fs_old_domains.*.name[count.index]}"
  type    = "A"
  alias {
    name    = "${var.elbDns}"
    zone_id = "${var.elbZone}"
    evaluate_target_health = false
  }
}
