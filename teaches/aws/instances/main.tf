variable security_group {}

resource "tls_private_key" "this" {
  algorithm = "RSA"
}

resource "aws_key_pair" "secure-app" {
  key_name   = "demo"
  public_key = tls_private_key.this.public_key_openssh 
}

resource "aws_instance" "secure-app" {
  key_name      = aws_key_pair.secure-app.key_name
  ami           = "ami-0006ee48a8c534af9"
  instance_type = "t2.micro"
  associate_public_ip_address = true
  subnet_id     = "subnet-27e41216"

  tags = {
    Name = "Secure APP"
  }

  vpc_security_group_ids = [
    var.security_group 
  ]

  connection {
    type        = "ssh"
    user        = "admin"
    private_key = file("key")
    host        = self.public_ip
  }

  ebs_block_device {
    device_name = "/dev/sda1"
    volume_type = "gp2"
    volume_size = 10 
  }
}

resource "aws_eip" "secure-app" {
  vpc      = true
  instance = aws_instance.secure-app.id
}
