locals {
  prod_forces = {
    policies = {
      aws = [
        {
          Sid    = "s3Write"
          Effect = "Allow"
          Action = ["*"]
          // This buckets and resources list belog to forces, so the wildcard
          // above is not dangerous
          Resource = [
            "arn:aws:s3:::fluidattacks-terraform-states-prod/break-build.tfstate",
            "arn:aws:s3:::fluidattacks-terraform-states-prod/forces*",
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

    keys = {
      prod_forces = {
        admins = [
          "prod_common",
        ]
        read_users = []
        users = [
          "prod_forces",
        ]
        tags = {
          "Name"               = "prod_forces"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_forces_aws" {
  source = "./modules/aws"

  name   = "prod_forces"
  policy = local.prod_forces.policies.aws

  tags = {
    "Name"               = "prod_forces"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

module "prod_forces_keys" {
  source   = "./modules/key"
  for_each = local.prod_forces.keys

  name       = each.key
  admins     = each.value.admins
  read_users = each.value.read_users
  users      = each.value.users
  tags       = each.value.tags
}
