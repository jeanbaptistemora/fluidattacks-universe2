variable "amiID" {}
variable "iType" {}
variable "sgId" {}
variable "snetId" {}
variable "kName" {}


resource "aws_instance" "fluidserves" {

  tags {
    Name = "fluidserves"
  }
  key_name = "${var.kName}"
  ami           = "${var.amiID}"
  instance_type = "${var.iType}"
  vpc_security_group_ids = ["${var.sgId}"]
  subnet_id = "${var.snetId}"

}
