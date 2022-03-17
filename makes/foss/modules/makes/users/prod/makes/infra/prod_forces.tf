locals {
  prod_forces = {
    policies = {
      aws = {
        Version = "2012-10-17"
        Statement = [
          {
            Sid    = "s3Write"
            Effect = "Allow"
            Action = ["*"]
            Resource = [
              "arn:aws:s3:::fluidattacks-terraform-states-prod/break-build.tfstate",
              "arn:aws:s3:::fluidattacks-terraform-states-prod/forces*",
            ]
          },
          {
            Sid    = "kmsRead"
            Effect = "Allow"
            Action = [
              "kms:CreateAlias",
              "kms:CreateKey",
              "kms:Describe*",
              "kms:Get*",
              "kms:List*",
              "kms:TagResource",
              "kms:UntagResource",
              "kms:UpdateAlias",
            ]
            Resource = ["*"]
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

    keys = {
      prod_forces = {
        admins = [
          "prod_makes",
        ]
        users = [
          "prod_forces",
        ]
        tags = {
          "Name"               = "prod_forces"
          "management:area"    = "cost"
          "management:product" = "makes"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_forces_aws" {
  source = "../../../modules/aws"

  name   = "prod_forces"
  policy = local.prod_forces.policies.aws

  tags = {
    "Name"               = "prod_forces"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

module "prod_forces_keys" {
  source   = "../../../modules/key"
  for_each = local.prod_forces.keys

  name   = each.key
  admins = each.value.admins
  users  = each.value.users
  tags   = each.value.tags
}

module "prod_forces_publish_credentials" {
  source = "../../../modules/publish_credentials"

  key_1     = module.prod_forces_aws.keys.1
  key_2     = module.prod_forces_aws.keys.2
  prefix    = "PROD_FORCES"
  protected = true
}
