resource "aws_route" "fs_netroute" {

  route_table_id         = "${aws_vpc.fs_vpc.main_route_table_id}"
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = "${aws_internet_gateway.fs_gateway.id}"
}
