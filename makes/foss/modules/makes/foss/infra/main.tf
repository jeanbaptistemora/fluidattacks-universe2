terraform {
  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "makes-foss.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.23.0"
    }
  }
  required_version = "~> 0.14.0"
}
