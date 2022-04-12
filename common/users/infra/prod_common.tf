locals {
  prod_common = {
    policies = {
      aws = {
        Version = "2012-10-17"
        Statement = [
          {
            Sid    = "allWrite"
            Effect = "Allow"
            Action = [
              "access-analyzer:*",
              "acm:*",
              "artifact:*",
              "autoscaling:*",
              "aws-marketplace:*",
              "aws-portal:*",
              "backup:*",
              "batch:*",
              "budgets:*",
              "ce:*",
              "cloudformation:*",
              "cloudwatch:*",
              "compute-optimizer:*",
              "cur:*",
              "dlm:*",
              "ds:*",
              "dynamodb:*",
              "ec2:*",
              "ecr:*",
              "ecs:*",
              "eks:*",
              "elasticache:*",
              "elasticloadbalancing:*",
              "events:*",
              "iam:*",
              "kms:*",
              "lambda:*",
              "logs:*",
              "pricing:*",
              "ram:*",
              "rds:*",
              "redshift:*",
              "redshift-serverless:*",
              "route53:*",
              "route53-recovery-control-config:*",
              "route53-recovery-readiness:*",
              "route53domains:*",
              "route53resolver:*",
              "s3:*",
              "sagemaker:*",
              "savingsplans:*",
              "secretsmanager:*",
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
    }

    keys = {
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

module "prod_common_publish_credentials" {
  source = "./modules/publish_credentials"

  providers = {
    gitlab = gitlab.product
  }

  key_1     = module.prod_common_aws.keys.1
  key_2     = module.prod_common_aws.keys.2
  prefix    = "PROD_COMMON"
  protected = true
}
