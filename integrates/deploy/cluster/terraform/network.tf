resource "aws_subnet" "region_a" {
  vpc_id                  = var.fluid_vpc_id
  availability_zone       = "${var.region}b"
  cidr_block              = "192.168.5.0/24"
  map_public_ip_on_launch = true

  tags = {
    "Name"                                      = "integrates-cluster-1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
    "management:type"                           = "production"
    "management:product"                        = "integrates"
  }
}

resource "aws_subnet" "region_b" {
  vpc_id                  = var.fluid_vpc_id
  availability_zone       = "${var.region}a"
  cidr_block              = "192.168.6.0/24"
  map_public_ip_on_launch = true

  tags = {
    "Name"                                      = "integrates-cluster-2"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
    "management:type"                           = "production"
    "management:product"                        = "integrates"
  }
}

resource "aws_subnet" "region_d" {
  vpc_id                  = var.fluid_vpc_id
  availability_zone       = "${var.region}d"
  cidr_block              = "192.168.7.0/24"
  map_public_ip_on_launch = true

  tags = {
    "Name"                                      = "integrates-cluster-3"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
    "management:type"                           = "production"
    "management:product"                        = "integrates"
  }
}
