terraform {
  backend "s3" {
    key     = "integrates.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {}

module "dynamodb" {
  source = "./dynamodb"
}
