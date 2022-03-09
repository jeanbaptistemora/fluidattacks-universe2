terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.4.0"
    }
    twilio = {
      source  = "twilio/twilio"
      version = "~> 0.13.2"
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

provider "twilio" {
  username = var.twilio_account_sid
  password = var.twilio_auth_token
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

module "verify-services" {
  source = "./verify-services"
}
