variable "sNetRegion" {}


resource "aws_subnet" "fs_subnet" {

  vpc_id            = "${aws_vpc.fs_vpc.id}"
  availability_zone = "${var.sNetRegion}"
  cidr_block        = "${cidrsubnet(aws_vpc.fs_vpc.cidr_block, 4, 1)}"
}
