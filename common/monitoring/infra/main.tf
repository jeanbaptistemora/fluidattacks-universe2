terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.50.0"
    }
    grafana = {
      source  = "grafana/grafana"
      version = "~> 1.33.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.3.0"
    }
    okta = {
      source  = "okta/okta"
      version = "~> 3.22.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "monitoring.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "grafana" {
  url  = "https://${aws_grafana_workspace.monitoring.endpoint}"
  auth = aws_grafana_workspace_api_key.monitoring.key
}

provider "okta" {
  org_name  = "fluidattacks"
  base_url  = "okta.com"
  api_token = var.oktaApiToken
}
