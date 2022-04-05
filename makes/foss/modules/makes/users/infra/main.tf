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
    key            = "makes-users-prod-makes.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
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
