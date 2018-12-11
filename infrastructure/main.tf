provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region = "${var.region}"
}

# Create from scratch
module "bucket" {
  source = "./bucket"
  fiBucket = "${var.fiBucket}"
  fsBucket = "${var.fsBucket}"
  fwBucket = "${var.fwBucket}"
}

# Create from scratch
module "iam" {
  source = "./iam"
  fwBucket = "${var.fwBucket}"
}

# #Create from scratch
# module "createNetwork" {
#   source = "./network"
#   sNetRegion = "${var.sNetRegion}"
#   cidr = "${var.cidr}"
#   runnerIp = "${var.runnerIp}"
# }

# Create Kubernetes cluster in existing VPC
module "eks" {
  source = "./eks"
  clusterInstanceType = "${var.clusterInstanceType}"
  clusterName  = "${var.clusterName}"
  eksAmiId     = "${var.eksAmiId}"
  eksSnetReg   = ["${var.eksSnetReg}"]
  region  = "${var.region}"
  rtbId   = "${var.rtbId}"
  vaultBucket = "${var.vaultBucket}"
  vpcCidr  = "${var.cidr}"
  vpcId    = "${var.vpcId}"
}

output "vaultKmsKey" {
  value     = "${module.eks.vaultKmsKey}"
  sensitive = true
}

# # Create with existing DB
module database {
  # source = "./database-outside"
  source = "./database"
  dbRegion="${var.dbRegion}"
  dbVpcId="${var.dbVpcId}"
  storageType="${var.storageType}"
  engine="${var.engine}"
  engineVersion="${var.engineVersion}"
  instanceClass="${var.instanceClass}"
  dbName="${var.dbName}"
  dbUser="${var.dbUser}"
  dbPass="${var.dbPass}"
  dbSnapId="${var.dbSnapId}"
}

output "dbEndpoint" {
  value = "dbInstance=\"${module.database.endpoint}\""
}

output "fwBucket" {
  value = "fwBucket=\"${module.bucket.webName}\""
}

output "fiBucket" {
  value = "fiBucket=\"${module.bucket.fiName}\""
}

# Create ElastiCache Redis Cluster
module "cache" {
  source = "./cache"
  cacheGroupId = "${var.cacheGroupId}"
  cacheGroupDescription  = "${var.cacheGroupDescription}"
  cacheNodeType     = "${var.cacheNodeType}"
  cacheCidr  = "${var.cacheCidr}"
  vpcId    = "${var.vpcId}"
  eksSnetReg   = ["${var.eksSnetReg}"]
  cacheParamGroupName  = "${var.cacheParamGroupName}"
}
