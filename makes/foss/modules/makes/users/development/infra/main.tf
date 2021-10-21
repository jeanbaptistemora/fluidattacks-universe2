terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.53.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "2.25.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "user-provision-development.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}

module "aws" {
  source  = "../../modules/aws"
  name    = "development"
  type    = "production"
  product = "makes"
  policy  = jsonencode(local.aws)
}

module "cloudflare" {
  source = "../../modules/cloudflare"
  name   = "development"
  policy = local.cloudflare
}

module "publish_credentials" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = module.aws.keys.1
  key_2        = module.aws.keys.2
  prefix       = "DEV"
  protected    = false
}
