terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.4.0"
    }
  }
}

variable "name" {
  type = string
}
variable "policies" { # Dict[str, List[Json]]
  default = {}
}
variable "tags" {
  type = map(string)
}
variable "assume_role_policy" { # List[Json]
  default = []
}

data "aws_eks_cluster" "common-k8s" {
  name = "common-k8s"
}
