variable "aws_s3_evidences_bucket" {
  type = string
}

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
  evidences_bucket_name = var.aws_s3_evidences_bucket
}

