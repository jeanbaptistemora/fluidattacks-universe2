terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.53.0"
    }
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = "3.7.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "makes-users-prod-services.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }
}

module "aws" {
  source = "../../../modules/aws"
  name   = "prod_services"
  policy = jsonencode(local.aws)

  tags = {
    "Name"               = "prod_services"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

provider "gitlab" {
  alias = "product"
  token = var.gitlab_token
}

provider "gitlab" {
  alias = "services"
  token = var.gitlab_token_services
}

module "publish_credentials_product" {
  source    = "../../../modules/publish_credentials"
  key_1     = module.aws.keys.1
  key_2     = module.aws.keys.2
  prefix    = "PROD_SERVICES"
  protected = true

  providers = {
    gitlab = gitlab.product
  }
}

module "publish_credentials_services" {
  source     = "../../../modules/publish_credentials"
  key_1      = module.aws.keys.1
  key_2      = module.aws.keys.2
  prefix     = "PROD"
  project_id = "4603023"
  protected  = true

  providers = {
    gitlab = gitlab.services
  }
}
