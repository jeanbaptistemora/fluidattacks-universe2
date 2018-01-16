
variable "allow_host_http_ports" {
  default = ["8080", "8000"]
}

resource "aws_eip" "fluidserves_eip" {

  instance = "${aws_instance.fluidserves.id}"
  vpc = true
  provisioner "local-exec" {
    command = "echo ${aws_eip.fluidserves_eip.public_ip} > ../ip_address.txt"
  }
}

resource "aws_eip_association" "eip_assoc" {

  instance_id   = "${aws_instance.fluidserves.id}"
  allocation_id = "${aws_eip.fluidserves_eip.id}"

  connection {
    host = "${aws_eip.fluidserves_eip.public_ip}"
    user = "ubuntu"
    private_key = "${file("vars/fluidtestingserves.pem")}"
  }

  provisioner "remote-exec" {
       inline = [
           "echo uname",
       ]
   }
}

resource "aws_security_group_rule" "ingress_http" {
  count = "${length(var.allow_host_http_ports)}"

  type        = "ingress"
  protocol    = "tcp"
  cidr_blocks = ["${join("",list(aws_eip.fluidserves_eip.public_ip,"/32"))}"]
  from_port   = "${element(var.allow_host_http_ports, count.index)}"
  to_port     = "${element(var.allow_host_http_ports, count.index)}"

  security_group_id = "${var.sgId}"
}

output "ip" {
  value = "${aws_eip.fluidserves_eip.public_ip}"

}
