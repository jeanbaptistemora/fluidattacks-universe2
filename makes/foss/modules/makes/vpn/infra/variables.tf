variable "cloudflare_email" {}
variable "cloudflare_api_key" {}
variable "vpnDataRaw" {}

data "cloudflare_ip_ranges" "cloudflare" {}
data "cloudflare_zones" "fluidattacks_com" {
  filter {
    name = "fluidattacks.com"
  }
}

locals {
  vpnData = {
    for client in jsondecode(var.vpnDataRaw) : client.id => client
  }
}

data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "batch_clone" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["batch_clone"]
  }
}
data "aws_subnet" "common" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["common"]
  }
}
variable "vpc_default_security_group_id" {
  default = "sg-0dbc8be47cc319b21"
}
