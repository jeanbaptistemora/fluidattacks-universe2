
provider "aws" {
  access_key = "${var.acc_key}"
  secret_key = "${var.sec_key}"
  region = "${var.reg}"
}

# Create from scratch
module "bucket" {
  source = "./bucket"
}

# Create from scratch
module "iam" {
  source = "./iam"
}

#Create from scratch
module "createNetwork" {
  source = "./network"
  sreg = "${var.sreg}"
  cdir = "${var.cdir}"
  ciIP = "${var.ciIP}"
}

# Create from scratch
module "ec2instance" {
  source = "./ec2"
  amiID = "${var.amiID}"
  iType = "${var.iType}"
  sreg = "${var.sreg}"
  sgId = "${module.createNetwork.sgId}"
  snetId = "${module.createNetwork.snetId}"
  kName = "${var.kName}"

}

# For Sura
module "ec2-peer" {
  source = "./ec2"
  amiID = "${var.amiID}"
  iType = "${var.iType}"
  sreg = "${var.sreg}"
  sgId = "sg-992bc3e4"
  snetId = "subnet-6a606433"
  kName = "${var.kName}"
}

# Create from scratch
# module "r53" {
#   source = "./dns"
#   server = "${module.ec2instance.ip}"
#   domain = "${var.zoneName}"
# }



output "variable_ip" {
  value = "server=\"${module.ec2-peer.ip}\""
}

output "instance_ip" {
  value = "${module.ec2-peer.ip}"
}
