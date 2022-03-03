terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.3.0"
    }
  }
}

variable "aws_cidr" {}
variable "client_endpoint" {}
variable "client_name" {}
variable "dns" {}
variable "routes" {}
variable "vpn_gateway_id" {}
variable "vpc_id" {}

variable "tags" {}

resource "aws_customer_gateway" "main" {
  bgp_asn     = 65000
  ip_address  = var.client_endpoint
  type        = "ipsec.1"
  device_name = var.client_name

  tags = var.tags
}

resource "aws_vpn_connection" "main" {
  vpn_gateway_id      = var.vpn_gateway_id
  customer_gateway_id = aws_customer_gateway.main.id
  type                = "ipsec.1"

  static_routes_only       = true
  local_ipv4_network_cidr  = "0.0.0.0/0"
  remote_ipv4_network_cidr = var.aws_cidr

  tags = var.tags
}

resource "aws_vpn_connection_route" "main" {
  for_each = toset(var.routes)

  destination_cidr_block = each.key
  vpn_connection_id      = aws_vpn_connection.main.id
}

module "dns" {
  for_each = {
    for dns in var.dns : dns.domain => dns
  }

  source = "../dns"
  domain = each.key
  hosts  = each.value.hosts
  vpc_id = var.vpc_id
  tags = merge(
    var.tags,
    {
      "Name" = each.key
    },
  )
}
