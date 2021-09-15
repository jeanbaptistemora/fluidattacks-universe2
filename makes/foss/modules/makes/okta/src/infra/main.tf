terraform {
  required_version = "~> 0.14.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.55.0"
    }
    okta = {
      source  = "okta/okta"
      version = "~> 3.13.7"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "makes-okta.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}

provider "aws" {}

provider "okta" {
  org_name  = "fluidattacks"
  base_url  = "okta.com"
  api_token = var.oktaApiToken
}
