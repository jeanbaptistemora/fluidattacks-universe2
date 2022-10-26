# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_route53_resolver_endpoint" "main" {
  name      = "vpn"
  direction = "INBOUND"

  security_group_ids = [
    var.vpc_default_security_group_id
  ]

  ip_address {
    subnet_id = data.aws_subnet.batch_clone.id
  }

  ip_address {
    subnet_id = data.aws_subnet.common.id
  }

  tags = {
    "Name"               = "vpn"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
