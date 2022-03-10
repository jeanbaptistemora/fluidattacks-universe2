terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.4.0"
    }
    checkly = {
      source  = "checkly/checkly"
      version = "1.4.2"
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
  account_id = var.checklyAccountId
  api_key    = var.checklyApiKey
}
