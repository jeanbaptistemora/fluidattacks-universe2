terraform {
  required_version = "~> 0.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.23.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "integrates-resources.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
}

module "dynamodb" {
  source = "./dynamodb"
}

module "cloudfront" {
  source                = "./cloudfront"
  bucket_name           = var.aws_s3_resources_bucket
  evidences_bucket_name = var.aws_s3_evidences_bucket
  reports_bucket_name   = var.aws_s3_reports_bucket
  build_bucket_name     = var.aws_s3_build_bucket
  forces_bucket_name    = var.aws_s3_forces_bucket
}

module "s3" {
  source                = "./s3"
  analytics_bucket_name = var.aws_s3_analytics_bucket
}

module "sqs" {
  source = "./sqs"
}

module "lambda" {
  source                                = "./lambda"
  sqs_id                                = module.sqs.sqs_id
  aws_lambda_send_mail_notification_zip = var.aws_lambda_send_mail_notification_zip
}
