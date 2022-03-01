resource "aws_vpn_gateway" "main" {
  vpc_id = aws_vpc.fluid-vpc.id

  tags = {
    "Name"               = "main"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

resource "aws_eip" "vpn" {
  vpc = true

  depends_on = [aws_internet_gateway.fluid-vpc]

  tags = {
    "Name"               = "vpn"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.vpn.id
  subnet_id     = aws_subnet.main["batch"].id

  tags = {
    "Name"               = "main"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }

  depends_on = [aws_internet_gateway.fluid-vpc]
}

module "vpn" {
  for_each = local.vpnData

  source          = "./modules/vpn"
  aws_cidr        = each.value.aws_cidr
  client_endpoint = each.value.client_endpoint
  client_name     = each.key
  routes          = each.value.routes
  vpn_gateway_id  = aws_vpn_gateway.main.id

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}
