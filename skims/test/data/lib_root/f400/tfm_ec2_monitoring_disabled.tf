resource "aws_instance" "foo" {
  monitoring                  = false
  instance_type               = "t2.micro"
  disable_api_termination     = true
  associate_public_ip_address = false
  security_groups             = ["test"]
  iam_instance_profile        = "ami-005e54dee72cc1d00"

  network_interface {
    network_interface_id = aws_network_interface.foo.id
    device_index         = 0
  }
  credit_specification {
    cpu_credits = "unlimited"
  }
}
