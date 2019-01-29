variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "cloudflare_email" {}
variable "cloudflare_token" {}
variable "cloudflare_org_id" {}
variable "dbInstance" {}
variable "elbDns" {}
variable "elbZone" {}
variable "domain" {}
variable "secDomains" {
  type = "list"
}
variable "region" {}

provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region = "${var.region}"
}

resource "aws_route53_zone" "fs_maindomain" {
  name = "${var.domain}"
  comment = "Dominio principal de FLUID"
}

resource "aws_route53_record" "mainA" {
  zone_id = "${aws_route53_zone.fs_maindomain.zone_id}"
  name    = "${aws_route53_zone.fs_maindomain.name}"
  type    = "A"
  alias {
    name    = "${var.elbDns}"
    zone_id = "${var.elbZone}"
    evaluate_target_health = false
  }
}

resource "aws_route53_zone" "fs_old_domains" {
  count   = 8
  name    = "${element(var.secDomains, count.index)}" 
  comment = "Dominio secundario de Fluid Attacks"
  force_destroy = true
}

resource "aws_route53_record" "old_domains_elb" {
  count   = 8
  zone_id = "${aws_route53_zone.fs_old_domains.*.zone_id[count.index]}"
  name    = "${aws_route53_zone.fs_old_domains.*.name[count.index]}"
  type    = "A"
  alias {
    name    = "${var.elbDns}"
    zone_id = "${var.elbZone}"
    evaluate_target_health = false
  }
}

provider "cloudflare" {
  email  = "${var.cloudflare_email}"
  token  = "${var.cloudflare_token}"
  org_id = "${var.cloudflare_org_id}"
}

resource "cloudflare_zone" "fluid_main_domain" {
  zone = "${var.domain}"
  plan = "free"
}

resource "cloudflare_zone" "fluid_secondary_domains" {
  count = "${length(var.secDomains)}"
  zone  = "${element(var.secDomains, count.index)}"
  plan  = "free"
}

resource "cloudflare_record" "main_domain_elb" {
  domain  = "${cloudflare_zone.fluid_main_domain.zone}"
  name    = "${cloudflare_zone.fluid_main_domain.zone}"
  type    = "CNAME"
  value   = "${var.elbDns}"
  proxied = true
}

resource "cloudflare_record" "secondary_domains_elb" {
  count   = "${length(var.secDomains)}"
  domain  = "${cloudflare_zone.fluid_secondary_domains.*.zone[count.index]}"
  name    = "${cloudflare_zone.fluid_secondary_domains.*.zone[count.index]}"
  type    = "CNAME"
  value   = "${var.elbDns}"
  proxied = true
}
