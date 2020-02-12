variable "dbRegion" {}
variable "dbVpcId" {}

data "aws_vpc" "selected" {
  id = var.dbVpcId
}


resource "aws_subnet" "rds_snet1" {

  vpc_id            = data.aws_vpc.selected.id
  availability_zone = "${var.dbRegion}a"
  cidr_block        = "172.30.10.0/24"
}

resource "aws_subnet" "rds_snet2" {

  vpc_id            = data.aws_vpc.selected.id
  availability_zone = "${var.dbRegion}b"
  cidr_block        = "172.30.11.0/24"
}

resource "aws_subnet" "rds_snet3" {

  vpc_id            = data.aws_vpc.selected.id
  availability_zone = "${var.dbRegion}c"
  cidr_block        = "172.30.12.0/24"
}

resource "aws_subnet" "rds_snet4" {

  vpc_id            = data.aws_vpc.selected.id
  availability_zone = "${var.dbRegion}d"
  cidr_block        = "172.30.13.0/24"
}

resource "aws_subnet" "rds_snet5" {

  vpc_id            = data.aws_vpc.selected.id
  availability_zone = "${var.dbRegion}e"
  cidr_block        = "172.30.14.0/24"
}
