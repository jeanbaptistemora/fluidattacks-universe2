terraform {
  backend "s3" {
    key     = "dns.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "dbInstance" {}
variable "elbDns" {}
variable "elbZone" {}
variable "domain" {}
variable "region" {}
variable "secDomains" {
  type = list(string)
}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
}

resource "aws_route53_zone" "fs_maindomain" {
  name    = var.domain
  comment = "Dominio principal de FLUID"
}

resource "aws_route53_record" "mainA" {
  zone_id = aws_route53_zone.fs_maindomain.zone_id
  name    = aws_route53_zone.fs_maindomain.name
  type    = "A"
  alias {
    name                   = var.elbDns
    zone_id                = var.elbZone
    evaluate_target_health = false
  }
}

resource "aws_route53_zone" "fs_old_domains" {
  count         = 8
  name          = element(var.secDomains, count.index)
  comment       = "Dominio secundario de Fluid Attacks"
  force_destroy = true
}

resource "aws_route53_record" "old_domains_elb" {
  count   = 8
  zone_id = aws_route53_zone.fs_old_domains[count.index].zone_id
  name    = aws_route53_zone.fs_old_domains[count.index].name
  type    = "A"
  alias {
    name                   = var.elbDns
    zone_id                = var.elbZone
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "old_domains_www" {
  count   = 8
  zone_id = aws_route53_zone.fs_old_domains[count.index].zone_id
  name    = "www.${aws_route53_zone.fs_old_domains[count.index].name}"
  type    = "CNAME"
  ttl     = "300"
  records = [aws_route53_zone.fs_old_domains[count.index].name]
}

