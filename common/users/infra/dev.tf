locals {
  dev = {
    policies = {
      aws = {
        Version = "2012-10-17"
        Statement = [
          {
            Sid    = "read"
            Effect = "Allow"
            Action = [
              "access-analyzer:Get*",
              "access-analyzer:List*",
              "access-analyzer:Validate*",
              "acm:Describe*",
              "acm:Get*",
              "acm:List*",
              "application-autoscaling:Describe*",
              "autoscaling:Describe*",
              "autoscaling:Get*",
              "backup:Describe*",
              "backup:Get*",
              "backup:List*",
              "batch:Describe*",
              "batch:List*",
              "cloudwatch:Describe*",
              "cloudwatch:Get*",
              "cloudwatch:List*",
              "dynamodb:DescribeContinuousBackups",
              "dynamodb:DescribeTable",
              "dynamodb:DescribeTimeToLive",
              "dynamodb:ListTagsOfResource",
              "ec2:Describe*",
              "ec2:Get*",
              "ecs:Describe*",
              "ecs:List*",
              "eks:Describe*",
              "eks:Get*",
              "elasticache:Describe*",
              "elasticache:List*",
              "es:Describe*",
              "es:Get*",
              "es:List*",
              "events:Describe*",
              "events:List*",
              "iam:Get*",
              "iam:List*",
              "kms:Describe*",
              "kms:Get*",
              "kms:List*",
              "lambda:Get*",
              "lambda:List*",
              "logs:Describe*",
              "logs:Filter*",
              "logs:Get*",
              "logs:List*",
              "redshift:Describe*",
              "route53:Get*",
              "route53:List*",
              "route53-recovery-control-config:Describe*",
              "route53-recovery-control-config:List*",
              "route53-recovery-readiness:Get*",
              "route53-recovery-readiness:List*",
              "route53domains:Get*",
              "route53domains:List*",
              "route53resolver:Get*",
              "route53resolver:List*",
              "sns:Get*",
              "sns:List*",
              "ssm:Describe*",
              "ssm:Get*",
              "ssm:List*",
              "sts:Decode*",
              "sts:Get*",
              "s3:Get*",
              "s3:List*",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "s3Write"
            Effect = "Allow"
            Action = [
              "s3:DeleteObject*",
              "s3:PutObject",
              "s3:PutObjectAcl",
            ]
            Resource = [
              "arn:aws:s3:::continuous-repositories/continuoustest*/*",
              "arn:aws:s3:::docs-dev.fluidattacks.com",
              "arn:aws:s3:::docs-dev.fluidattacks.com/*",
              "arn:aws:s3:::fluidintegrates.analytics/*atfluid",
              "arn:aws:s3:::fluidintegrates.analytics/*atfluid/*",
              "arn:aws:s3:::integrates.front.development.fluidattacks.com",
              "arn:aws:s3:::integrates.front.development.fluidattacks.com/*",
              "arn:aws:s3:::skims.data",
              "arn:aws:s3:::skims.data/*",
              "arn:aws:s3:::web.eph.fluidattacks.com",
              "arn:aws:s3:::web.eph.fluidattacks.com/*",
            ]
          },
          {
            Sid    = "dynamodbLock"
            Effect = "Allow"
            Action = [
              "dynamodb:DeleteItem",
              "dynamodb:GetItem",
              "dynamodb:PutItem",
            ]
            Resource = ["arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"]
          },
          {
            Sid      = "dynamodbList"
            Effect   = "Allow"
            Action   = ["dynamodb:ListTables"]
            Resource = ["arn:aws:dynamodb:us-east-1:205810638802:table/*"]
          },
          {
            Sid    = "dynamodbReadSkims"
            Effect = "Allow"
            Action = [
              "dynamodb:Get*",
              "dynamodb:ListTagsOfResource",
              "dynamodb:Scan",
            ]
            Resource = ["arn:aws:dynamodb:us-east-1:205810638802:table/skims*"]
          },
          {
            Sid    = "sqsRead"
            Effect = "Allow"
            Action = [
              "sqs:GetQueueUrl",
              "sqs:GetQueueAttributes",
              "sqs:ListQueueTags",
              "sqs:ListQueues",
            ]
            Resource = [
              "arn:aws:sqs:us-east-1:205810638802:skims-*",
              "arn:aws:sqs:us-east-1:205810638802:celery",
            ]
          },
        ]
      }
      cloudflare = {
        account = {
          effect = "allow"
          permission_groups = [
            data.cloudflare_api_token_permission_groups.all.permissions["Workers Scripts Read"],
          ]
          resources = {
            "com.cloudflare.api.account.*" = "*"
          }
        }
        accountZone = {
          effect = "allow"
          permission_groups = [
            data.cloudflare_api_token_permission_groups.all.permissions["Zone Read"],
            data.cloudflare_api_token_permission_groups.all.permissions["DNS Read"],
            data.cloudflare_api_token_permission_groups.all.permissions["Workers Routes Read"],
            data.cloudflare_api_token_permission_groups.all.permissions["Cache Purge"],
            data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Read"],
            data.cloudflare_api_token_permission_groups.all.permissions["Firewall Services Read"],
          ]
          resources = {
            "com.cloudflare.api.account.zone.*" = "*"
          }
        }
      }
    }

    keys = {
      dev = {
        admins = [
          "prod_common",
        ]
        users = [
          "dev",
          "prod_airs",
          "prod_docs",
          "prod_forces",
          "prod_integrates",
          "prod_melts",
          "prod_observes",
          "prod_services",
          "prod_skims",
          "prod_sorts",
        ]
        tags = {
          "Name"               = "dev"
          "management:area"    = "innovation"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "dev_aws" {
  source = "./modules/aws"

  name   = "dev"
  policy = local.dev.policies.aws

  extra_assume_role_policies = [
    {
      Sid    = "commonClusterAssumePolicy",
      Effect = "Allow",
      Principal = {
        Federated = join(
          "/",
          [
            "arn:aws:iam::205810638802:oidc-provider",
            replace(data.aws_eks_cluster.common.identity[0].oidc[0].issuer, "https://", ""),
          ]
        )
      },
      Action = "sts:AssumeRoleWithWebIdentity",
      Condition = {
        StringEquals = {
          join(
            ":",
            [
              replace(data.aws_eks_cluster.common.identity[0].oidc[0].issuer, "https://", ""),
              "sub",
            ]
          ) : "system:serviceaccount:development:dev"
        },
      },
    },
  ]

  tags = {
    "Name"               = "dev"
    "management:area"    = "innovation"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

module "dev_keys" {
  source   = "./modules/key"
  for_each = local.dev.keys

  name   = each.key
  admins = each.value.admins
  users  = each.value.users
  tags   = each.value.tags
}

module "dev_publish_credentials_product" {
  source = "./modules/publish_credentials"

  providers = {
    gitlab = gitlab.universe
  }

  key_1     = module.dev_aws.keys.1
  key_2     = module.dev_aws.keys.2
  prefix    = "DEV"
  protected = false
}

module "dev_publish_credentials_services" {
  source = "./modules/publish_credentials"

  providers = {
    gitlab = gitlab.services
  }

  key_1      = module.dev_aws.keys.1
  key_2      = module.dev_aws.keys.2
  prefix     = "DEV"
  project_id = "4603023"
  protected  = false
}

module "dev_cloudflare" {
  source = "./modules/cloudflare"

  name   = "dev"
  policy = local.dev.policies.cloudflare
}
