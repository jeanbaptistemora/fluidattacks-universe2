terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.4.0"
    }
  }
}

variable "aws_role" {}
variable "policies" {}
variable "tags" {}
