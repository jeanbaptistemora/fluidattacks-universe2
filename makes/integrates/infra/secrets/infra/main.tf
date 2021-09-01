terraform {
  required_version = "~> 0.14.0"

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

module "external" {
  source = "../../../../../makes/utils/terraform-modules/external-data"

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
    "integrates-dev",
    "integrates-prod",
  ]
}
