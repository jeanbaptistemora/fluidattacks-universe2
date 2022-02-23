locals {
  subnets = [
    {
      name                    = "ci"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = false
      new_bits                = 6
      tags                    = {}
    },
    {
      name                    = "free"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags                    = {}
    },
    {
      name                    = "batch"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = true
      new_bits                = 7
      tags                    = {}
    },
    {
      name                    = "common"
      availability_zone       = "us-east-1b"
      map_public_ip_on_launch = false
      new_bits                = 7
      tags                    = {}
    },
    {
      name                    = "k8s_1"
      availability_zone       = "us-east-1b"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/makes-k8s" = "shared"
        "kubernetes.io/role/elb"          = "1"
      }
    },
    {
      name                    = "k8s_2"
      availability_zone       = "us-east-1a"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/makes-k8s" = "shared"
        "kubernetes.io/role/elb"          = "1"
      }
    },
    {
      name                    = "k8s_3"
      availability_zone       = "us-east-1d"
      map_public_ip_on_launch = true
      new_bits                = 6
      tags = {
        "kubernetes.io/cluster/makes-k8s" = "shared"
        "kubernetes.io/role/elb"          = "1"
      }
    },
  ]
}

module "subnet_addrs" {
  source  = "hashicorp/subnets/cidr"
  version = "1.0.0"

  base_cidr_block = aws_vpc.fluid-vpc.cidr_block
  networks        = local.subnets
}

resource "aws_subnet" "main" {
  for_each = {
    for subnet in local.subnets : subnet.name => subnet
  }

  vpc_id                  = aws_vpc.fluid-vpc.id
  cidr_block              = module.subnet_addrs.network_cidr_blocks[each.key]
  availability_zone       = each.value.availability_zone
  map_public_ip_on_launch = each.value.map_public_ip_on_launch

  tags = merge(
    {
      "Name"               = each.key
      "management:area"    = "cost"
      "management:product" = "makes"
      "management:type"    = "product"
    },
    each.value.tags,
  )
}
