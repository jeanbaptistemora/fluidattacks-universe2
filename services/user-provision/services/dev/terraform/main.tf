terraform {
  backend "s3" {
    bucket  = "fluidattacks-terraform-states-dev"
    key     = "user-provision-continuous-dev.tfstate"
    region  = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform_state_lock"
  }
}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  version    = ">= 2.11"
  region     = var.region
}
