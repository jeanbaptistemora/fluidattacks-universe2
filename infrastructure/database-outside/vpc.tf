resource "aws_vpc" "fsexams_vpc" {

  cidr_block = "172.30.0.0/16"
  tags {
    Name = "FLUIDExamsVPC"
  }
}
