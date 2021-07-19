data "aws_caller_identity" "current" {}


variable "region" {
  default = "us-east-1"
}

variable "skimsQueues" {}

variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}

# Reused infrastructure

variable "batch_vpc_id" {
  default = "vpc-0ea1c7bd6be683d2d"
}
