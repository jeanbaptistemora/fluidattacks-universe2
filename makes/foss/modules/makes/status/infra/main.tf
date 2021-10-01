terraform {
  required_version = "~> 0.14.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.53.0"
    }
    checkly = {
      source  = "checkly/checkly"
      version = "1.2.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "makes-status.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }
}

provider "aws" {}

provider "checkly" {
  api_key = var.checklyApiKey
}