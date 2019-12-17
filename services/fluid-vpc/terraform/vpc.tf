resource "aws_vpc" "fluid-vpc" {
  cidr_block       = "10.0.0.0/16"
  tags = {
    Name = "fluid-vpc"
  }
}
