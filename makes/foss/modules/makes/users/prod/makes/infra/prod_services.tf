locals {
  prod_services = {
    policies = {
      aws = {
        Version = "2012-10-17"
        Statement = [
          {
            Sid    = "generalRead"
            Effect = "Allow"
            Action = [
              "iam:Get*",
              "iam:List*",
              "kms:CreateAlias",
              "kms:CreateKey",
              "kms:Describe*",
              "kms:Get*",
              "kms:List*",
              "kms:TagResource",
              "kms:UntagResource",
              "kms:UpdateAlias",
              "kms:DeleteAlias",
              "s3:Get*",
              "s3:List*",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "generalWrite"
            Effect = "Allow"
            Action = ["*"]
            Resource = [
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/continuous*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/secure-notes*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/continuous*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/continuous*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/secure-notes*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/continuous*",
              "arn:aws:s3:::continuous*",
              "arn:aws:s3:::continuous*/*",
              "arn:aws:s3:::fluidattacks-terraform-states-prod/break*",
              "arn:aws:s3:::fluidattacks-terraform-states-prod/continuous*",
              "arn:aws:s3:::fluidattacks-terraform-states-prod/services*",
            ]
          },
          {
            Sid    = "sagemakerWrite"
            Effect = "Allow"
            Action = [
              "sagemaker:*",
            ]
            Resource = ["*"]
          },
          {
            Sid      = "dynamoWrite"
            Effect   = "Allow"
            Action   = ["dynamodb:*"]
            Resource = ["*"]
          },
          {
            Sid    = "dynamoReadGroups"
            Effect = "Allow"
            Action = [
              "dynamodb:Scan",
            ]
            Resource = [
              "arn:aws:dynamodb:us-east-1:205810638802:table/FI_projects",
            ]
          }
        ]
      }
    }
  }
}

module "prod_services_aws" {
  source = "../../../modules/aws"

  name   = "prod_services"
  policy = local.prod_services.policies.aws

  tags = {
    "Name"               = "prod_services"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

module "prod_services_publish_credentials_product" {
  source = "../../../modules/publish_credentials"

  providers = {
    gitlab = gitlab.product
  }

  key_1     = module.prod_services_aws.keys.1
  key_2     = module.prod_services_aws.keys.2
  prefix    = "PROD_SERVICES"
  protected = true
}

module "prod_services_publish_credentials_services" {
  source = "../../../modules/publish_credentials"

  providers = {
    gitlab = gitlab.services
  }

  key_1      = module.prod_services_aws.keys.1
  key_2      = module.prod_services_aws.keys.2
  prefix     = "PROD"
  project_id = "4603023"
  protected  = true
}
