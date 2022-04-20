data "aws_caller_identity" "current" {}
data "aws_ec2_instance_type" "instance" {
  instance_type = "c5ad.xlarge"
}
data "aws_ec2_instance_type" "instance_large" {
  instance_type = "c5ad.2xlarge"
}

variable "region" {
  default = "us-east-1"
}

variable "skimsQueues" {}

variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
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
