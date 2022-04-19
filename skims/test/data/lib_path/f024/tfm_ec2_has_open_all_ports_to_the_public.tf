resource "aws_security_group_rule" "not_vulnerable" {
  security_group_id = "sg-123456"
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = "127.0.0.1/32"
  prefix_list_ids   = ["pl-12c4e678"]

}

resource "aws_security_group" "not_vulnerable" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"
  vpc_id      = "someid"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = "127.0.0.1/32"
  }

  egress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "udp"
    cidr_blocks     = ["127.0.0.1/32"]
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
  from_port         = 0
  to_port           = 65535
  protocol          = "-1"
  cidr_blocks       = "0.0.0.0/0"
  prefix_list_ids   = ["pl-12c4e678"]

}


resource "aws_security_group" "vulnerable" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"
  vpc_id      = "someid"

  ingress {
    from_port        = 443
    to_port          = 446
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "udp"
    cidr_blocks     = ["127.0.0.1/32"]
    prefix_list_ids = ["pl-12c4e678"]
  }

  tags = {
    method = "aws.terraform.ec2.allows_all_outbound_traffic"
    Name   = "aws.terraform.allows_all_outbound_traffic"
  }
}
