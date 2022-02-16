module "vpn" {
  for_each = local.vpnData

  source          = "./modules/vpn"
  aws_cidr        = each.value.aws_cidr
  client_cidr     = each.value.client_cidr
  client_endpoint = each.value.client_endpoint
  client_name     = each.key
  vpc_id          = aws_vpc.fluid-vpc.id

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}
