terraform {
  required_version = "~> 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.23.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "observes-infra.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}

module "external" {
  source = "../../../../../../makes/utils/terraform-modules/external-data"

  aws_iam_roles = [
    "observes_dev",
    "observes_prod",
    "makes_prod",
  ]
  aws_iam_users = [
    "observes-dev",
    "observes-prod",
  ]
}
