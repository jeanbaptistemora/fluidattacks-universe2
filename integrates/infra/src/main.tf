terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.20.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 3.10.0"
    }
    twilio = {
      source  = "twilio/twilio"
      version = "~> 0.13.2"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "integrates-prod-database.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

provider "twilio" {
  username = var.twilio_account_sid
  password = var.twilio_auth_token
}
