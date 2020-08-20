# AWS vars
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "region" {
  default = "us-east-1"
}
variable "sNetRegion" {
  default = "us-east-1b"
}

# S3 vars
variable "fsBucket" {
  default = "servestf"
}

#EC2 vars
variable "clusterInstanceType" {
  default = "m5a.xlarge"
}

# Net Vars
variable "cidr" {
  default = "192.168.100.0/24"
}
variable "vpcSecondaryCidr" {
  default = "192.168.104.0/21"
}
variable "vpcId" {
  default = "vpc-53ea4637"
}

# EKS Vars
variable "clusterName" {
  default = "FluidServes"
}
variable "eksAmiId" {
  default = "ami-0abcb9f9190e867ab"
}
variable "nodeStorageSize" {
  default = "50"
}
variable "rtbId" {
  default = "rtb-a74ad5c3"
}
variable "eksSnetReg" {
  type = list(string)
  default = [
    "us-east-1d",
    "us-east-1e",
  ]
}
variable "eksSnetRegSecondary" {
  type = list(string)
  default = [
    "us-east-1a",
    "us-east-1b",
  ]
}
