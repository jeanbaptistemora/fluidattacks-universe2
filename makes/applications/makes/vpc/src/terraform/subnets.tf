resource "aws_subnet" "subnet-autoscaling-ci" {
  vpc_id            = aws_vpc.fluid-vpc.id
  cidr_block        = "192.168.0.0/22"
  availability_zone = "us-east-1a"

  tags = {
    "Name"               = "autoscaling-ci"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_subnet" "subnet-common" {
  vpc_id            = aws_vpc.fluid-vpc.id
  cidr_block        = "192.168.10.0/23"
  availability_zone = "us-east-1b"

  tags = {
    "Name"               = "common"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}
