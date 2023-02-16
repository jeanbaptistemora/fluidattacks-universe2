resource "aws_security_group_rule" "not_vulnerable" {
  security_group_id = "sg-123456"
  type              = "ingress"
  from_port         = 443
  to_port           = 445
  protocol          = "tcp"
  cidr_blocks       = "0.0.0.0/0"
  prefix_list_ids   = ["pl-12c4e678"]

}

resource "aws_security_group" "not_vulnerable" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"
  vpc_id      = "someid"

  ingress {
    from_port   = 0
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = "127.0.0.1/32"
  }

  egress {
    from_port       = 19
    to_port         = 20
    protocol        = "udp"
    cidr_blocks     = ["0.0.0.0/0"]
    prefix_list_ids = ["pl-12c4e678"]
  }

  tags = {
    method = "aws.terraform.ec2.allows_all_outbound_traffic"
    Name   = "aws.terraform.allows_all_outbound_traffic"
  }
}

resource "aws_security_group_rule" "vulnerable" {
  security_group_id = "sg-123456"
  type              = "ingress"
  from_port         = 21
  to_port           = 21
  protocol          = "-1"
  cidr_blocks       = "0.0.0.0/0"
  prefix_list_ids   = ["pl-12c4e678"]

}
