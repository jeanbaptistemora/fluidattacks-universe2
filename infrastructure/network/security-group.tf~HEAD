variable "allow_all_http_ports" {
  default = ["80", "7090", "7001", "443","8081"]
}

resource "aws_security_group" "fs_secgroup" {

  name        = "fluidserves sec_group"
  description = "Used in the terraform"
  vpc_id      = "${aws_vpc.fs_vpc.id}"

  egress {
          from_port   = 0
          to_port     = 0
          protocol    = "-1"
          cidr_blocks = ["0.0.0.0/0"]
          }
}

resource "aws_security_group_rule" "ingress_http" {
  count = "${length(var.allow_all_http_ports)}"

  type        = "ingress"
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
  from_port   = "${element(var.allow_all_http_ports, count.index)}"
  to_port     = "${element(var.allow_all_http_ports, count.index)}"

  security_group_id = "${aws_security_group.fs_secgroup.id}"
}
