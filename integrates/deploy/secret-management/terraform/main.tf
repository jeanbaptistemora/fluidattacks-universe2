terraform {
  required_version = "~> 0.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.23.0"
    }
  }

  backend "s3" {
    bucket         = "fluidattacks-terraform-states-prod"
    key            = "integrates-secret-management.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform_state_lock"
  }

}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
}

module "external" {
  source = "../../../../makes/utils/terraform-modules/external-data"

  aws_iam_roles = [
    "integrates-dev",
    "integrates-prod",
    "makes_prod",
  ]
  aws_iam_policies = {
    "dynamodb-admin"         = ["aws", "AmazonDynamoDBFullAccess"]
    "cloudwatch-push"        = ["aws", "service-role/AmazonAPIGatewayPushToCloudWatchLogs"]
    "integrates-dev-policy"  = ["us", "user-provision/integrates-dev-policy"]
    "integrates-prod-policy" = ["us", "user-provision/integrates-prod-policy"]
  }
  aws_iam_users = [
    "FLUIDServes_TF",
    "integrates-dev",
    "integrates-prod",
  ]
}
