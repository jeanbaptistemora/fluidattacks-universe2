terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.4.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 3.10.0"
    }
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = "3.12.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "makes-users-prod-integrates.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }
}

module "aws" {
  source = "../../../modules/aws"
  name   = "prod_integrates"
  policy = local.aws

  tags = {
    "Name"               = "prod_integrates"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

module "cloudflare" {
  source = "../../../modules/cloudflare"
  name   = "prod_integrates"
  policy = local.cloudflare
}

provider "gitlab" {
  token = var.gitlab_token
}

module "publish_credentials" {
  source    = "../../../modules/publish_credentials"
  key_1     = module.aws.keys.1
  key_2     = module.aws.keys.2
  prefix    = "PROD_INTEGRATES"
  protected = true
}
