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
variable "policy" {}
variable "tags" {}
variable "extra_assume_role_policies" {
  default = []
}
