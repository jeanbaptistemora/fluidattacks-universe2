locals {
  prod_airs = {
    policies = {
      aws = [
        {
          Sid    = "s3Write"
          Effect = "Allow"
          Action = ["*"]
          // This buckets and resources list belog to airs, so the wildcard
          // above is not dangerous
          Resource = [
            "arn:aws:s3:::fluidattacks.com",
            "arn:aws:s3:::fluidattacks.com/*",
            "arn:aws:s3:::fluidattacks-terraform-states-prod/airs*",
            "arn:aws:s3:::web.eph.fluidattacks.com",
            "arn:aws:s3:::web.eph.fluidattacks.com/*",
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
      prod_airs = {
        admins = [
          "prod_common",
        ]
        read_users = []
        users = [
          "prod_airs",
        ]
        tags = {
          "Name"               = "prod_airs"
          "management:area"    = "cost"
          "management:product" = "airs"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_airs_aws" {
  source = "./modules/aws"

  name   = "prod_airs"
  policy = local.prod_airs.policies.aws

  tags = {
    "Name"               = "prod_airs"
    "management:area"    = "cost"
    "management:product" = "airs"
    "management:type"    = "product"
  }
}

module "prod_airs_keys" {
  source   = "./modules/key"
  for_each = local.prod_airs.keys

  name       = each.key
  admins     = each.value.admins
  read_users = each.value.read_users
  users      = each.value.users
  tags       = each.value.tags
}

module "prod_airs_cloudflare" {
  source = "./modules/cloudflare"

  name   = "prod_airs"
  policy = local.prod_airs.policies.cloudflare
}
