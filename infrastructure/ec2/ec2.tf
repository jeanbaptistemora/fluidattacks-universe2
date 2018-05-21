variable "amiID" {}
variable "iType" {}
variable "sgId" {}
variable "snetId" {}
variable "kName" {}
variable "sreg" {}


resource "aws_instance" "fluidserves" {

  tags {
    Name = "fluidserves"
  }
  key_name = "${var.kName}"
  ami           = "${var.amiID}"
  instance_type = "${var.iType}"
  iam_instance_profile   = "${module.iam.fs-cloudwatchagent}"
  vpc_security_group_ids = ["${var.sgId}"]
  subnet_id = "${var.snetId}"
  root_block_device {
    volume_size = 100
  }
}
