resource "aws_subnet" "subnet-autoscaling-ci" {
  vpc_id            = aws_vpc.fluid-vpc.id
  cidr_block        = "192.168.0.0/22"
  availability_zone = "us-east-1a"

  tags = {
    "Name"               = "autoscaling-ci"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

resource "aws_subnet" "subnet-common" {
  vpc_id            = aws_vpc.fluid-vpc.id
  cidr_block        = "192.168.10.0/23"
  availability_zone = "us-east-1b"

  tags = {
    "Name"               = "common"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

resource "aws_subnet" "default" {
  availability_zone       = "us-east-1a"
  cidr_block              = "192.168.8.0/23"
  map_public_ip_on_launch = true
  vpc_id                  = aws_vpc.fluid-vpc.id

  tags = {
    "Name"               = "batch"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

resource "aws_subnet" "region_a" {
  vpc_id                  = aws_vpc.fluid-vpc.id
  availability_zone       = "us-east-1b"
  cidr_block              = "192.168.12.0/22"
  map_public_ip_on_launch = true

  tags = {
    "Name"                            = "makes-k8s-1"
    "kubernetes.io/cluster/makes-k8s" = "shared"
    "kubernetes.io/role/elb"          = "1"
    "management:area"                 = "cost"
    "management:product"              = "makes"
    "management:type"                 = "product"
  }
}

resource "aws_subnet" "region_b" {
  vpc_id                  = aws_vpc.fluid-vpc.id
  availability_zone       = "us-east-1a"
  cidr_block              = "192.168.16.0/22"
  map_public_ip_on_launch = true

  tags = {
    "Name"                            = "makes-k8s-2"
    "kubernetes.io/cluster/makes-k8s" = "shared"
    "kubernetes.io/role/elb"          = "1"
    "management:area"                 = "cost"
    "management:product"              = "makes"
    "management:type"                 = "product"
  }
}

resource "aws_subnet" "region_d" {
  vpc_id                  = aws_vpc.fluid-vpc.id
  availability_zone       = "us-east-1d"
  cidr_block              = "192.168.20.0/22"
  map_public_ip_on_launch = true

  tags = {
    "Name"                            = "makes-k8s-3"
    "kubernetes.io/cluster/makes-k8s" = "shared"
    "kubernetes.io/role/elb"          = "1"
    "management:area"                 = "cost"
    "management:product"              = "makes"
    "management:type"                 = "product"
  }
}
