resource "aws_security_group" "aws_batch_compute_environment_security_group" {
  name   = "aws_batch_compute_environment_security_group"
  vpc_id = data.aws_vpc.main.id

  # AWS manage this things and it's unknown what source port, protocol or ip
  # will access the machine
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name"               = "aws_batch_compute_environment_security_group"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
