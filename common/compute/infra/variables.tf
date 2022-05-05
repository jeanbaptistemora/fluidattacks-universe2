data "aws_caller_identity" "current" {}
data "aws_ec2_instance_type" "instance" {
  instance_type = "c5ad.xlarge"
}
data "aws_ec2_instance_type" "instance_large" {
  instance_type = "c5ad.2xlarge"
}
data "local_file" "skims_queues" {
  filename = var.skimsQueues
}

variable "region" {
  default = "us-east-1"
}

variable "skimsQueues" {}

variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}

# Environment

variable "productApiToken" {
  sensitive = true
}

locals {
  environments = {
    unlimited_spot = {
      max_vcpus = 10000
      type      = "SPOT"
    }
    unlimited_dedicated = {
      max_vcpus = 10000
      type      = "EC2"
    }
    limited_spot = {
      max_vcpus = 50
      type      = "SPOT"
    }
    limited_dedicated = {
      max_vcpus = 50
      type      = "EC2"
    }
  }
}

# Reused infrastructure

data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "batch_clone" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["batch_clone"]
  }
}
data "aws_subnet" "batch_main" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["batch_main"]
  }
}
data "aws_iam_role" "prod_common" {
  name = "prod_common"
}
