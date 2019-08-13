terraform {
  backend "s3" {
    key     = "staging.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  access_key = var.aws_innovation_access_key
  secret_key = var.aws_innovation_secret_key
  region     = var.region
}

resource "aws_vpc" "dev_vpc" {
  cidr_block           = var.cidr
  enable_dns_hostnames = true
  tags = {
    Name = "FluidDevVPC"
  }
}

resource "aws_subnet" "dev_subnet" {
  count             = 5
  availability_zone = var.dbZones[count.index]
  cidr_block        = cidrsubnet(aws_vpc.dev_vpc.cidr_block, 4, count.index)
  vpc_id            = aws_vpc.dev_vpc.id
  tags = {
    Name = "DevSubNet"
  }
}

resource "aws_internet_gateway" "dev_gateway" {
  vpc_id = aws_vpc.dev_vpc.id
}

resource "aws_route" "dev_netroute" {
  route_table_id         = aws_vpc.dev_vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.dev_gateway.id
}

