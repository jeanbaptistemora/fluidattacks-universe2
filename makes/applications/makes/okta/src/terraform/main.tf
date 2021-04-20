terraform {
  required_version = "~> 0.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.23.0"
    }
    okta = {
      source  = "oktadeveloper/okta"
      version = "~> 3.10"
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

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
}

provider "okta" {
  org_name  = "fluidattacks"
  base_url  = "okta.com"
  api_token = var.okta_api_token
}
