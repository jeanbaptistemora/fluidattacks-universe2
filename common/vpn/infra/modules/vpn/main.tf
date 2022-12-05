terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.4.0"
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

locals {
  config = {
    dpd_timeout_action = "restart"
    startup_action     = "start"
    ike = [
      "ikev1",
      "ikev2",
    ]
    phase1_groups = [
      2,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23,
      24,
    ]
    phase1_encryption = [
      "AES128",
      "AES128-GCM-16",
      "AES256",
      "AES256-GCM-16",
    ]
    phase1_integrity = [
      "SHA1",
      "SHA2-256",
      "SHA2-384",
      "SHA2-512",
    ]
    phase2_groups = [
      2,
      5,
      14,
      15,
      16,
      17,
      18,
      19,
      20,
      21,
      22,
      23,
      24,
    ]
    phase2_encryption = [
      "AES128",
      "AES128-GCM-16",
      "AES256",
      "AES256-GCM-16",
    ]
    phase2_integrity = [
      "SHA1",
      "SHA2-256",
      "SHA2-384",
      "SHA2-512",
    ]
  }
}

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

  tunnel1_dpd_timeout_action           = local.config.dpd_timeout_action
  tunnel1_startup_action               = local.config.startup_action
  tunnel1_ike_versions                 = local.config.ike
  tunnel1_phase1_dh_group_numbers      = local.config.phase1_groups
  tunnel1_phase1_encryption_algorithms = local.config.phase1_encryption
  tunnel1_phase1_integrity_algorithms  = local.config.phase1_integrity
  tunnel1_phase2_dh_group_numbers      = local.config.phase2_groups
  tunnel1_phase2_encryption_algorithms = local.config.phase2_encryption
  tunnel1_phase2_integrity_algorithms  = local.config.phase2_integrity

  tunnel2_dpd_timeout_action           = local.config.dpd_timeout_action
  tunnel2_startup_action               = local.config.startup_action
  tunnel2_ike_versions                 = local.config.ike
  tunnel2_phase1_dh_group_numbers      = local.config.phase1_groups
  tunnel2_phase1_encryption_algorithms = local.config.phase1_encryption
  tunnel2_phase1_integrity_algorithms  = local.config.phase1_integrity
  tunnel2_phase2_dh_group_numbers      = local.config.phase2_groups
  tunnel2_phase2_encryption_algorithms = local.config.phase2_encryption
  tunnel2_phase2_integrity_algorithms  = local.config.phase2_integrity

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
