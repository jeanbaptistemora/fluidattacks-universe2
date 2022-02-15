resource "aws_launch_configuration" "example" {
  instance_type = "t2.micro"
  root_block_device {
    encrypted = false
  }
}
