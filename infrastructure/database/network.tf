variable "dbreg" {}
variable "vpcId" {}

data "aws_vpc" "selected" {
  id = "${var.vpcId}"
}


resource "aws_subnet" "rds_snet1" {

  vpc_id            = "${data.aws_vpc.selected.id}"
  availability_zone = "${var.dbreg}a"
  cidr_block        = "172.30.10.0/24"
}

resource "aws_subnet" "rds_snet2" {

  vpc_id            = "${data.aws_vpc.selected.id}"
  availability_zone = "${var.dbreg}b"
  cidr_block        = "172.30.11.0/24"
}

resource "aws_subnet" "rds_snet3" {

  vpc_id            = "${data.aws_vpc.selected.id}"
  availability_zone = "${var.dbreg}c"
  cidr_block        = "172.30.12.0/24"
}

resource "aws_subnet" "rds_snet4" {

  vpc_id            = "${data.aws_vpc.selected.id}"
  availability_zone = "${var.dbreg}d"
  cidr_block        = "172.30.13.0/24"
}

resource "aws_subnet" "rds_snet5" {

  vpc_id            = "${data.aws_vpc.selected.id}"
  availability_zone = "${var.dbreg}e"
  cidr_block        = "172.30.14.0/24"
}
