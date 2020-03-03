terraform {
  backend "s3" {
    bucket  = "servestf"
    key     = "production.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
}

# Create from scratch
module "bucket" {
  source                               = "./bucket"
  region                               = var.region
  fsBucket                             = var.fsBucket
  fwBucket                             = var.fwBucket
}

# Create from scratch
module "iam" {
  source               = "./iam"
  fwBucket             = var.fwBucket
  fsBucket             = var.fsBucket
  region               = var.region
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
  vaultBucket         = var.vaultBucket
  vpcCidr             = var.cidr
  vpcSecondaryCidr    = var.vpcSecondaryCidr
  vpcId               = var.vpcId
}

output "vaultKmsKey" {
  value     = module.eks.vaultKmsKey
  sensitive = true
}

output "fwBucket" {
  value = "fwBucket=\"${module.bucket.webName}\""
}
