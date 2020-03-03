# AWS vars
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "region" {}
variable "sNetRegion" {}

# S3 vars
variable "fsBucket" {}
variable "fwBucket" {}
variable "vaultBucket" {}

#EC2 vars
variable "clusterInstanceType" {}

# Net Vars
variable "cidr" {}
variable "vpcSecondaryCidr" {}
variable "vpcId" {}

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
