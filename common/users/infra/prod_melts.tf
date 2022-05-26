locals {
  prod_melts = {
    policies = {
      aws = {
        Version = "2012-10-17"
        Statement = [
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

  name   = "prod_melts"
  policy = local.prod_melts.policies.aws

  tags = {
    "Name"               = "prod_melts"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

module "prod_melts_publish_credentials" {
  source = "./modules/publish_credentials"

  providers = {
    gitlab = gitlab.product
  }

  key_1     = module.prod_melts_aws.keys.1
  key_2     = module.prod_melts_aws.keys.2
  prefix    = "PROD_MELTS"
  protected = true
}
