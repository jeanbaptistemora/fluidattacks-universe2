terraform {
  required_version = "~> 1.0"
  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "makes-roles-for-users.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }
}


provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  version    = "~> 4.4.0"
  region     = "us-east-1"
}
