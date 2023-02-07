resource "aws_instance" "secure" {
  ami                         = "ami-04b9e92b5572fa0d1"
  availability_zone           = "us-east-1a"
  ebs_optimized               = false
  instance_type               = "t2.small"
  monitoring                  = false
  key_name                    = "generic_aws_key"
  subnet_id                   = "subnet-00f969b107a8e55b4"
  vpc_security_group_ids      = ["sg-0f98371a3f6cad87e"]
  associate_public_ip_address = false

  disable_api_termination = true

  iam_instance_profile = "test_profile"

  tags = {
    method = "aws.terraform.ec2.has_unencrypted_volumes"
    Name   = "aws.ec2_unencrypted"
  }
}

resource "aws_instance" "insecure" {
  ami                         = "ami-04b9e92b5572fa0d1"
  availability_zone           = "us-east-1a"
  ebs_optimized               = false
  instance_type               = "t2.small"
  monitoring                  = false
  key_name                    = "generic_aws_key"
  subnet_id                   = "subnet-00f969b107a8e55b4"
  associate_public_ip_address = true

  disable_api_termination = true

  tags = {
    method = "aws.ec2.has_unencrypted_volumes"
    Name   = "aws.ec2_unencrypted"
  }
}
