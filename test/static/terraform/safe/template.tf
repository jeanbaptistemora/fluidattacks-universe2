resource "aws_instance" "i-0d1583d0c02a9bb47" {
  ami                         = "ami-04b9e92b5572fa0d1"
  availability_zone           = "us-east-1a"
  ebs_optimized               = false
  instance_type               = "t2.small"
  monitoring                  = false
  key_name                    = "generic_aws_key"
  subnet_id                   = "subnet-00f969b107a8e55b4"
  vpc_security_group_ids      = ["sg-0f98371a3f6cad87e"]
  associate_public_ip_address = true
  private_ip                  = "10.0.0.44"
  source_dest_check           = true

  root_block_device {
    volume_type           = "gp2"
    volume_size           = 20
    delete_on_termination = true
    encrypted = true
  }

  ebs_block_device {
    device_name           = "/dev/sdg"
    volume_type           = "gp2"
    volume_size           = 20
    delete_on_termination = true
    encrypted = true
  }

  tags = {
    method  = "aws.terraform.ec2.has_unencrypted_volumes"
    Name    = "aws.ec2_unencrypted"
  }
}
