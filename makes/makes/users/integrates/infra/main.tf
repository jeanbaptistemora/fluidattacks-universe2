terraform {
  required_version = "~> 0.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.53.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "2.20.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "user-provision-integrates.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}
