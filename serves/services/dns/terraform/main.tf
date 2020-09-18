terraform {
  required_version = "~> 0.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 2.70.0"
    }
  }

  backend "s3" {
    bucket  = "fluidattacks-terraform-states-prod"
    key     = "dns.tfstate"
    region  = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform_state_lock"
  }

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
