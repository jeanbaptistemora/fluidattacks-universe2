variable security_group_secure_app {}
variable security_group_intranet {}

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
  iam_instance_profile = aws_iam_instance_profile.ec2-profile.name

  tags = {
    Name = "Secure APP"
  }

  vpc_security_group_ids = [
    var.security_group_secure_app 
  ]

  connection {
    type        = "ssh"
    user        = "admin"
    private_key = file("key")
    host        = self.public_ip
  }
}

resource "aws_iam_instance_profile" "ec2-profile" {
  name = "ec2_profile"
  role = aws_iam_role.ec2-role.name
}

resource "aws_eip" "secure-app" {
  vpc      = true
  instance = aws_instance.secure-app.id
}

resource "aws_instance" "intranet" {
  key_name      = aws_key_pair.secure-app.key_name
  ami           = "ami-0006ee48a8c534af9"
  instance_type = "t2.micro"
  associate_public_ip_address = true
  subnet_id     = "subnet-02ab05a7f7d913450"

  tags = {
    Name = "Intranet"
  }

  vpc_security_group_ids = [
    var.security_group_intranet 
  ]

  connection {
    type        = "ssh"
    user        = "admin"
    private_key = file("key")
    host        = self.public_ip
  }
}

resource "aws_eip" "intranet" {
  vpc      = true
  instance = aws_instance.intranet.id
}
