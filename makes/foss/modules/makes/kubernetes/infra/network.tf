resource "aws_subnet" "region_a" {
  vpc_id                  = var.fluid_vpc_id
  availability_zone       = "us-east-1b"
  cidr_block              = "192.168.12.0/22"
  map_public_ip_on_launch = true

  tags = {
    "Name"                                      = "makes-k8s-1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
    "management:type"                           = "production"
    "management:product"                        = "makes"
  }
}

resource "aws_subnet" "region_b" {
  vpc_id                  = var.fluid_vpc_id
  availability_zone       = "us-east-1a"
  cidr_block              = "192.168.16.0/22"
  map_public_ip_on_launch = true

  tags = {
    "Name"                                      = "makes-k8s-2"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
    "management:type"                           = "production"
    "management:product"                        = "makes"
  }
}

resource "aws_subnet" "region_d" {
  vpc_id                  = var.fluid_vpc_id
  availability_zone       = "us-east-1d"
  cidr_block              = "192.168.20.0/22"
  map_public_ip_on_launch = true

  tags = {
    "Name"                                      = "makes-k8s-3"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
    "management:type"                           = "production"
    "management:product"                        = "makes"
  }
}
