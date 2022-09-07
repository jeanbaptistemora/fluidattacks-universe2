# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_vpc" "fluid-vpc" {
  cidr_block           = "192.168.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    "Name"               = "fluid-vpc"
    "Management:Area"    = "cost"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}

resource "aws_internet_gateway" "fluid-vpc" {
  vpc_id = aws_vpc.fluid-vpc.id

  tags = {
    "Name"               = "fluid-vpc"
    "Management:Area"    = "cost"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}

resource "aws_route" "fluid-vpc-internet" {
  route_table_id         = aws_vpc.fluid-vpc.default_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.fluid-vpc.id
}
