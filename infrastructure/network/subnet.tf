variable "sreg" {}


resource "aws_subnet" "fs_subnet" {

  vpc_id            = "${aws_vpc.fs_vpc.id}"
  availability_zone = "${var.sreg}"
  cidr_block        = "${cidrsubnet(aws_vpc.fs_vpc.cidr_block, 4, 1)}"
}
