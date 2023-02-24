terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.4.0"
    }
  }
}

variable "name" {}
variable "policies" {}
variable "tags" {}
variable "assume_role_policy" {
  default = []
}

data "aws_eks_cluster" "common-k8s" {
  name = "common-k8s"
}
