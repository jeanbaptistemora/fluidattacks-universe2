
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
  sgId = "${var.sgroupId}"
  snetId = "${var.snetId}"
  kName = "${var.kName}"
}

# # Create with existing DB
module database {
  source = "./database"
  dbreg="${var.dbreg}"
  vpcId="${var.db_vpcId}"
  storage_type="${var.storage_type}"
  engine="${var.engine}"
  engine_ver="${var.engine_ver}"
  instance_class="${var.instance_class}"
  db_name="${var.db_name}"
  db_user="${var.db_user}"
  db_pass="${var.db_pass}"
  db_id="${var.db_id}"
}

output "variable_db" {
  value = "db_instance=\"${module.database.endpoint}\""
}

output "variable_ip" {
  value = "server=\"${module.ec2-peer.ip}\""
}

output "instance_ip" {
  value = "${module.ec2-peer.ip}"
}
