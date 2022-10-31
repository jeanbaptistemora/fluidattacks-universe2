# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

terraform {
  required_version = "~> 1.0"

  required_providers {
    auth0 = {
      source  = "auth0/auth0"
      version = ">= 0.34" # Refer to docs for latest version
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.4.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 3.10.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "airs.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "cloudflare" {
  account_id = var.cloudflareAccountId
  api_token  = var.cloudflareApiToken
}

provider "auth0" {
  domain        = var.auth0ClientDomain
  client_id     = var.auth0ClientId
  client_secret = var.auth0ClientSecret
}
