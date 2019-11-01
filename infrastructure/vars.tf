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
variable "vpcSecondaryCidr" {}
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
variable "eksSnetRegSecondary" {
  type = list(string)
}

# ElastiCache Vars
variable "cacheGroupId" {}
variable "cacheGroupDescription" {}
variable "cacheNodeType" {}
variable "cacheParamGroupName" {}
