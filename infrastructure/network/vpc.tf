variable "cdir" {}

resource "aws_vpc" "fs_vpc" {

  cidr_block = "${var.cdir}"
  tags {
    Name = "FLUIDServesVPC"
  }
}
