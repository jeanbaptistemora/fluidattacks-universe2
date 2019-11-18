terraform {
  backend "s3" {
    bucket = "fluidattacks-terraform-states"
    key     = "user-provision-integrates.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  version = ">= 2.11"
  region  = "us-east-1"
}
