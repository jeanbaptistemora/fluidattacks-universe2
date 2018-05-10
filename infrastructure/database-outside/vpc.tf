resource "aws_vpc" "fsexams_vpc" {

  cidr_block = "172.30.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true
  tags {
    Name = "FLUIDExamsVPC"
  }
}

resource "aws_internet_gateway" "fsexams_vpc_gw" {
  vpc_id = "${aws_vpc.fsexams_vpc.id}"
  tags {
    Name = "FLUIDExamsVPC GW"
  }
}
