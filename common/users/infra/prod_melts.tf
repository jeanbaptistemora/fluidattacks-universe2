locals {
  prod_melts = {
    policies = {
      aws = {
        MetlsPolicy = [
          {
            Sid    = "s3Write"
            Effect = "Allow"
            Action = ["*"]
            // This buckets and resources list belog to melts, so the wildcard
            // above is not dangerous
            Resource = [
              "arn:aws:s3:::fluidattacks-terraform-states-prod/melts*",
            ]
          },
          {
            Sid    = "dynamoWrite"
            Effect = "Allow"
            Action = [
              "dynamodb:DeleteItem",
              "dynamodb:GetItem",
              "dynamodb:PutItem",
            ]
            Resource = [
              var.terraform_state_lock_arn,
            ]
          },
        ]
      }
    }
  }
}

module "prod_melts_aws" {
  source = "./modules/aws"

  name     = "prod_melts"
  policies = local.prod_melts.policies.aws

  tags = {
    "Name"               = "prod_melts"
    "management:area"    = "cost"
    "management:product" = "melts"
    "management:type"    = "product"
  }
}
