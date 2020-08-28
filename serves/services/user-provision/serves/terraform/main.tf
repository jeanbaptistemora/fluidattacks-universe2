terraform {
  required_version = ">= 0.13"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 2.70.0"
    }
  }

  backend "s3" {
    bucket  = "fluidattacks-terraform-states-prod"
    key     = "user-provision-serves.tfstate"
    region  = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform_state_lock"
  }

}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
}
