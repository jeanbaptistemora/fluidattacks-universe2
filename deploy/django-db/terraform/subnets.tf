resource "aws_subnet" "region-a" {
  vpc_id            = var.fluid-vpc-id
  availability_zone = "${var.region}a"
  cidr_block        = "192.168.4.0/25"
}

resource "aws_subnet" "region-b" {
  vpc_id            = var.fluid-vpc-id
  availability_zone = "${var.region}b"
  cidr_block        = "192.168.4.128/25"
}
