# AWS vars
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "region" {}
variable "sNetRegion" {}
variable "dbRegion" {}

# S3 vars
variable "fsBucket" {}
variable "fwBucket" {}
variable "fiBucket" {}
variable "vaultBucket" {}

# gitlabCI
variable "runnerIp" {}

#EC2 vars
variable "clusterInstanceType" {}

# Net Vars
variable "cidr" {}
variable "vpcId" {}

# DB Vars
variable "dbVpcId" {}
variable "storageType" {}
variable "engine" {}
variable "engineVersion" {}
variable "instanceClass" {}
variable "dbName" {}
variable "dbUser" {}
variable "dbPass" {}
variable "dbSnapId" {}

# EKS Vars
variable "clusterName" {}
variable "eksAmiId" {}
variable "nodeStorageSize" {}
variable "rtbId" {}
variable "eksSnetReg" {
  type = list(string)
}

# ElastiCache Vars
variable "cacheGroupId" {}
variable "cacheGroupDescription" {}
variable "cacheNodeType" {}
variable "cacheParamGroupName" {}

# Asserts IAM, ACR and S3 vars
variable "asserts-bucket" {}
variable "asserts_projects" {
  type = list(string)
  default = [
    "temp1",
    "temp2",
    "temp3",
  ]
}
