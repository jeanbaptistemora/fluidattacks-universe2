locals {
  prod_docs = {
    policies = {
      aws = {
        Version = "2012-10-17"
        Statement = [
          {
            Sid    = "s3Write"
            Effect = "Allow"
            Action = ["*"]
            Resource = [
              "arn:aws:s3:::docs.fluidattacks.com",
              "arn:aws:s3:::docs.fluidattacks.com/*",
              "arn:aws:s3:::docs-dev.fluidattacks.com",
              "arn:aws:s3:::docs-dev.fluidattacks.com/*",
              "arn:aws:s3:::fluidattacks-terraform-states-prod/docs*",
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
      cloudflare = {
        account = {
          effect = "allow"
          permission_groups = [
            data.cloudflare_api_token_permission_groups.all.permissions["Workers Scripts Write"],
          ]
          resources = {
            "com.cloudflare.api.account.*" = "*"
          }
        }
        accountZone = {
          effect = "allow"
          permission_groups = [
            data.cloudflare_api_token_permission_groups.all.permissions["Workers Routes Write"],
            data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Write"],
            data.cloudflare_api_token_permission_groups.all.permissions["DNS Write"],
          ]
          resources = {
            "com.cloudflare.api.account.zone.*" = "*"
          }
        }
      }
    }

    keys = {
      prod_docs = {
        admins = [
          "prod_makes",
        ]
        users = [
          "prod_docs",
        ]
        tags = {
          "Name"               = "prod_docs"
          "management:area"    = "cost"
          "management:product" = "makes"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_docs_aws" {
  source = "../../../modules/aws"

  name   = "prod_docs"
  policy = local.prod_docs.policies.aws

  tags = {
    "Name"               = "prod_docs"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

module "prod_docs_keys" {
  source   = "../../../modules/key"
  for_each = local.prod_docs.keys

  name   = each.key
  admins = each.value.admins
  users  = each.value.users
  tags   = each.value.tags
}

module "prod_docs_publish_credentials" {
  source = "../../../modules/publish_credentials"

  providers = {
    gitlab = gitlab.product
  }

  key_1     = module.prod_docs_aws.keys.1
  key_2     = module.prod_docs_aws.keys.2
  prefix    = "PROD_DOCS"
  protected = true
}

module "prod_docs_cloudflare" {
  source = "../../../modules/cloudflare"

  name   = "prod_docs"
  policy = local.prod_docs.policies.cloudflare
}
