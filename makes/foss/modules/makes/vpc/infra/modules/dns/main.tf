terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.4.0"
    }
  }
}

variable "domain" {}
variable "hosts" {}
variable "vpc_id" {}

variable "tags" {}

resource "aws_route53_zone" "main" {
  name = var.domain

  vpc {
    vpc_id = var.vpc_id
  }

  tags = var.tags
}

resource "aws_route53_record" "main" {
  for_each = {
    for host in var.hosts : host.name => host
  }

  zone_id = aws_route53_zone.main.zone_id
  name    = "${each.key}.${var.domain}"
  type    = "A"
  ttl     = "300"
  records = [each.value.ip]
}
