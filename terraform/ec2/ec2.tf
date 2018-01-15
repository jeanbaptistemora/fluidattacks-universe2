variable amiID {}
variable iType {}
variable sgId {}
variable snetId {}

resource "aws_instance" "fluidserves" {
  tags {
    Name = "fluidserves"
  }
  ami           = "ami-2757f631"
  instance_type = "t2.micro"
  vpc_security_group_ids = ["sg-5c0dd622"]
  subnet_id = "subnet-ae51a5f4"
}

resource "aws_eip" "ip" {
  instance = "${aws_instance.example.id}"
  vpc = true
  provisioner "local-exec" {
    command = "echo ${aws_eip.ip.public_ip} > ../ip_address.txt"
  }
}

output "ip" {
  value = "${aws_eip.ip.public_ip}"
} 
