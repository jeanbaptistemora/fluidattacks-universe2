variable "aws_s3_resources_bucket" {
  type = string
}

terraform {
  backend "s3" {
    key     = "integrates.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
}

module "dynamodb" {
  source = "./dynamodb"
}

module "cloudfront" {
  source      = "./cloudfront"
  bucket_name = var.aws_s3_resources_bucket
}

