terraform {
  backend "s3" {
    bucket  = "servestf"
    key     = "production.tfstate"
    region  = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform_state_lock"
  }
}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
}

# Create from scratch
module "bucket" {
  source   = "./bucket"
  region   = var.region
  fsBucket = var.fsBucket
}

# Create Kubernetes cluster in existing VPC
module "eks" {
  source              = "./eks"
  clusterInstanceType = var.clusterInstanceType
  clusterName         = var.clusterName
  eksAmiId            = var.eksAmiId
  eksSnetReg          = var.eksSnetReg
  eksSnetRegSecondary = var.eksSnetRegSecondary
  nodeStorageSize     = var.nodeStorageSize
  region              = var.region
  rtbId               = var.rtbId
  vpcCidr             = var.cidr
  vpcSecondaryCidr    = var.vpcSecondaryCidr
  vpcId               = var.vpcId
}
