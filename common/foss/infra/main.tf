# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

terraform {
  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "makes-foss.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.4.0"
    }
  }
  required_version = "~> 1.0"
}

provider "aws" {
  region = "us-east-1"
}
