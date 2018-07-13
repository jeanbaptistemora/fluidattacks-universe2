
provider "aws" {
  access_key = "${var.acc_key}"
  secret_key = "${var.sec_key}"
  region = "${var.reg}"
}

# Create from scratch
module "bucket" {
  source = "./bucket"
  bucketName = "${var.bucket}"
  webBucket = "${var.webBucket}"
  fiBucket = "${var.fiBucket}"
}

# Create from scratch
module "iam" {
  source = "./iam"
  webBucket = "${var.webBucket}"
}

# #Create from scratch
# module "createNetwork" {
#   source = "./network"
#   sreg = "${var.sreg}"
#   cidr = "${var.cidr}"
#   ciIP = "${var.ciIP}"
# }
# 
# # Create from scratch
# module "ec2instance" {
#   source = "./ec2"
#   amiID = "${var.amiID}"
#   iType = "${var.iType}"
#   sreg = "${var.sreg}"
#   sgId = "${module.createNetwork.sgId}"
#   snetId = "${module.createNetwork.snetId}"
#   kName = "${var.kName}"
# 
# }
# output "variable_ip" {
#   value = "server=\"${module.ec2instance.ip}\""
# }
# output "instance_ip" {
#   value = "${module.ec2instance.ip}"
# }


# new with cron and peer
module "ec2-cron" {
  source = "./ec2"
  amiID = "${var.amiID}"
  iType = "${var.iType}"
  sreg = "${var.sreg}"
  sgId = "${var.sgroupId}"
  snetId = "${var.snetId}"
  kName = "${var.kName}"
  iamProfile = "${module.iam.fs-cloudwatchagent}"
}
output "variable_ip" {
  value = "server=\"${module.ec2-cron.ip}\""
}
output "instance_ip" {
  value = "${module.ec2-cron.ip}"
}

# Create Kubernetes cluster in existing VPC
module "eks" {
  source = "./eks"
  clusterName = "${var.clusterName}"
  eksSnetReg  = ["${var.eksSnetReg}"]
  rtbId   = "${var.rtbId}"
  vpcCidr = "${var.cidr}"
  vpcId   = "${var.vpcId}"
}


# # Create with existing DB
module database {
  # source = "./database-outside"
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

output "variable_web" {
  value = "bucket=\"${module.bucket.webName}\""
}

output "variable_integrates" {
  value = "bucket-integrates=\"${module.bucket.fiName}\""
}




# CREDS
output "fis3integrationID" {
  sensitive = true
value = "${module.iam.fis3integrationID}"
}

output "cloudwatchID" {
  sensitive = true
value = "${module.iam.cloudwatchID}"
}

output "fluidintegratesdynamoID" {
  sensitive = true
value = "${module.iam.fluidintegratesdynamoID}"
}

output "fws3userID" {
  sensitive = true
value = "${module.iam.fws3userID}"
}

#
output "fis3integrationSECRET" {
  sensitive = true
value = "${module.iam.fis3integrationSECRET}"
}

output "cloudwatchSECRET" {
  sensitive = true
value = "${module.iam.cloudwatchSECRET}"
}

output "fluidintegratesdynamoSECRET" {
  sensitive = true
value = "${module.iam.fluidintegratesdynamoSECRET}"
}

output "fws3userSECRET" {
  sensitive = true
value = "${module.iam.fws3userSECRET}"
}
