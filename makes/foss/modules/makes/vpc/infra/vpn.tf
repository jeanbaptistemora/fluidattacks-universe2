resource "aws_vpn_gateway" "main" {
  vpc_id = aws_vpc.fluid-vpc.id

  tags = {
    "Name"               = "main"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

module "vpn" {
  for_each = local.vpnData

  source          = "./modules/vpn"
  aws_cidr        = each.value.aws_cidr
  client_cidr     = each.value.client_cidr
  client_endpoint = each.value.client_endpoint
  client_name     = each.key
  vpn_gateway_id  = aws_vpn_gateway.main.id

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}
