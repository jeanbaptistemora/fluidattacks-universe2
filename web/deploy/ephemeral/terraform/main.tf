terraform {
  backend "s3" {
    bucket  = "fluidattacks-terraform-states-prod"
    key     = "web-ephemeral.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  version    = "2.70.0"
  region     = var.region
}
