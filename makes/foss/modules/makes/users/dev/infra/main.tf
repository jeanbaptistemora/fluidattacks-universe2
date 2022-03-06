terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.74.3"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "2.25.0"
    }
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = "3.7.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "makes-users-dev.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}

module "aws" {
  source = "../../modules/aws"
  name   = "dev"
  policy = local.aws

  tags = {
    "Name"               = "dev"
    "management:area"    = "innovation"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

module "key" {
  source = "../../modules/key"

  name = "dev"
  admins = [
    "prod_makes",
  ]
  users = [
    "dev",
    "prod_airs",
    "prod_docs",
    "prod_forces",
    "prod_integrates",
    "prod_melts",
    "prod_observes",
    "prod_services",
    "prod_skims",
    "prod_sorts",
  ]

  tags = {
    "Name"               = "dev"
    "management:area"    = "innovation"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

module "cloudflare" {
  source = "../../modules/cloudflare"
  name   = "dev"
  policy = local.cloudflare
}

provider "gitlab" {
  alias = "product"
  token = var.gitlab_token
}

provider "gitlab" {
  alias = "services"
  token = var.gitlab_token_services
}

module "publish_credentials" {
  source    = "../../modules/publish_credentials"
  key_1     = module.aws.keys.1
  key_2     = module.aws.keys.2
  prefix    = "DEV"
  protected = false

  providers = {
    gitlab = gitlab.product
  }
}

module "publish_credentials_services" {
  source     = "../../modules/publish_credentials"
  key_1      = module.aws.keys.1
  key_2      = module.aws.keys.2
  prefix     = "DEV"
  project_id = "4603023"
  protected  = false

  providers = {
    gitlab = gitlab.services
  }
}
