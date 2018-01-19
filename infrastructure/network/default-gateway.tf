resource "aws_internet_gateway" "fs_gateway" {

  vpc_id = "${aws_vpc.fs_vpc.id}"
}
