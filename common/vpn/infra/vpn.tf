# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_vpn_gateway" "main" {
  vpc_id = data.aws_vpc.main.id

  tags = {
    "Name"               = "main"
    "Management:Area"    = "cost"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}

module "vpn" {
  for_each = local.vpnData

  source          = "./modules/vpn"
  aws_cidr        = each.value.aws_cidr
  client_endpoint = each.value.client_endpoint
  client_name     = each.key
  dns             = each.value.dns
  routes          = each.value.routes
  vpn_gateway_id  = aws_vpn_gateway.main.id
  vpc_id          = data.aws_vpc.main.id

  tags = {
    "Name"               = each.key
    "Management:Area"    = "cost"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}
