# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

locals {
  prod_common = {
    policies = {
      aws = [
        {
          Sid    = "allWrite"
          Effect = "Allow"
          Action = [
            "access-analyzer:*",
            "acm:*",
            "autoscaling:*",
            "aws-marketplace:*",
            "aws-portal:*",
            "backup:*",
            "batch:*",
            "budgets:*",
            "ce:*",
            "cloudformation:*",
            "cloudwatch:*",
            "cur:*",
            "dynamodb:*",
            "ec2:*",
            "ecs:*",
            "eks:*",
            "elasticache:*",
            "elasticloadbalancing:*",
            "es:*",
            "events:*",
            "firehose:*",
            "grafana:*",
            "iam:*",
            "kinesis:*",
            "kinesisanalytics:*",
            "kms:*",
            "lambda:*",
            "logs:*",
            "pricing:*",
            "ram:*",
            "rds:*",
            "redshift:*",
            "redshift-data:*",
            "redshift-serverless:*",
            "route53:*",
            "route53-recovery-control-config:*",
            "route53-recovery-readiness:*",
            "route53domains:*",
            "route53resolver:*",
            "s3:*",
            "sagemaker:*",
            "savingsplans:*",
            "schemas:*",
            "secretsmanager:*",
            "serverlessrepo:*",
            "servicequotas:*",
            "sns:*",
            "sqs:*",
            "ssm:*",
            "sts:*",
            "support:*",
            "tag:*",
          ]
          Resource = ["*"]
        },
      ]

    }

    keys = {
      common_google = {
        admins = [
          "prod_common",
        ]
        users = [
          "dev",
        ]
        tags = {
          "Name"               = "common_google"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
      common_okta = {
        admins = [
          "prod_common",
        ]
        users = [
          "dev",
        ]
        tags = {
          "Name"               = "common_okta"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
      common_status = {
        admins = [
          "prod_common",
        ]
        users = [
          "dev",
        ]
        tags = {
          "Name"               = "common_status"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
      common_vpn = {
        admins = [
          "prod_common",
        ]
        users = [
          "dev",
        ]
        tags = {
          "Name"               = "common_vpn"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
      prod_common = {
        admins = [
          "prod_common",
        ]
        users = []
        tags = {
          "Name"               = "prod_common"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_common_aws" {
  source = "./modules/aws"

  name   = "prod_common"
  policy = local.prod_common.policies.aws

  assume_role_policy = [
    {
      Sid    = "AssumeRolePolicy",
      Effect = "Allow",
      Principal = {
        Service = [
          "batch.amazonaws.com",
          "events.amazonaws.com",
          "spotfleet.amazonaws.com",
        ],
      },
      Action = "sts:AssumeRole",
    },
  ]

  tags = {
    "Name"               = "prod_common"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

module "prod_common_keys" {
  source   = "./modules/key"
  for_each = local.prod_common.keys

  name   = each.key
  admins = each.value.admins
  users  = each.value.users
  tags   = each.value.tags
}
