terraform {
  backend "s3" {
    bucket = "fluidattacks-terraform-states"
    key     = "user-provision.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  access_key = "aws_access_key"
  secret_key = "aws_secret_key"
  version = ">= 2.11"
  region  = "us-east-1"
}
