variable "cidr" {}

resource "aws_vpc" "fs_vpc" {

  cidr_block = "${var.cidr}"
  tags {
    Name = "FLUIDServesVPC"
  }
}
