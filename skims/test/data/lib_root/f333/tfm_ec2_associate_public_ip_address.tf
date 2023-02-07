resource "aws_launch_template" "vulnerable" {
  name                                 = "foo"
  instance_type                        = "t2.micro"
  kernel_id                            = "test"
  key_name                             = "test"
  disable_api_termination              = "false"
  instance_initiated_shutdown_behavior = "terminate"
  security_groups                      = []

  monitoring {
    enabled = true
  }

  network_interfaces {
    associate_public_ip_address = true
  }

  placement {
    availability_zone = "us-west-2a"
  }

  ram_disk_id = "test"
}

resource "aws_launch_template" "not_vulnerable" {
  name                                 = "foo"
  instance_type                        = "t2.micro"
  kernel_id                            = "test"
  key_name                             = "test"
  disable_api_termination              = "false"
  instance_initiated_shutdown_behavior = "terminate"
  security_groups                      = []

  monitoring {
    enabled = true
  }

  network_interfaces {
    associate_public_ip_address = false
  }

  placement {
    availability_zone = "us-west-2a"
  }
  ram_disk_id = "test"
}

resource "aws_instance" "vulnerable" {
  ami                         = "ami-04b9e92b5572fa0d1"
  availability_zone           = "us-east-1a"
  instance_type               = "t2.small"
  key_name                    = "generic_aws_key"
  subnet_id                   = "subnet-00f969b107a8e55b4"
  associate_public_ip_address = true
  private_ip                  = "10.0.0.44"
  iam_instance_profile        = "example"
  security_groups             = []

  tags = {
    method = "aws.ec2.has_unencrypted_volumes"
    Name   = "aws.ec2_unencrypted"
  }
}


resource "aws_instance" "not_vulnerable" {
  ami                         = "ami-04b9e92b5572fa0d1"
  availability_zone           = "us-east-1a"
  instance_type               = "t2.small"
  key_name                    = "generic_aws_key"
  subnet_id                   = "subnet-00f969b107a8e55b4"
  associate_public_ip_address = false
  private_ip                  = "10.0.0.44"
  iam_instance_profile        = "example"
  security_groups             = []

  tags = {
    method = "aws.ec2.has_unencrypted_volumes"
    Name   = "aws.ec2_unencrypted"
  }
}
