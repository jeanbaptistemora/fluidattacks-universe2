terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.23.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "2.25.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "dns.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}

provider "aws" {}

provider "cloudflare" {
  email   = var.cloudflareEmail
  api_key = var.cloudflareApiKey
}
