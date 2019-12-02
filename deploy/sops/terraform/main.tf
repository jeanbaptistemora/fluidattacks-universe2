terraform {
  backend "s3" {
    bucket  = "fluidattacks-terraform-states-dev"
    key     = "integrates-dev-sops.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  access_key = var.dev_aws_access_key
  secret_key = var.dev_aws_secret_key
  version    = ">= 2.11"
  region     = var.region
}
