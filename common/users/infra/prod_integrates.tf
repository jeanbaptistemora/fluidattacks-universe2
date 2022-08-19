locals {
  prod_integrates = {
    policies = {
      aws = [
        {
          Sid    = "iamRead"
          Effect = "Allow"
          Action = [
            "iam:List*",
            "iam:Get*",
            "iam:Create*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "iamWrite"
          Effect = "Allow"
          Action = ["*"]
          Resource = [
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable",
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/integrates*",
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:policy/integrates*",
          ]
        },
        {
          Sid    = "elasticacheRead"
          Effect = "Allow"
          Action = [
            "elasticache:Describe*",
            "elasticache:List*",
            "elasticache:CreateReplicationGroup",
            "elasticache:CreateCacheSecurityGroup",
            "elasticache:CreateCacheSubnetGroup",
            "elasticache:AddTagsToResource",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "elasticacheWrite"
          Effect = "Allow"
          Action = ["*"]
          Resource = [
            "arn:aws:elasticache:${var.region}:${data.aws_caller_identity.main.account_id}:cluster:integrates-*",
            "arn:aws:elasticache:${var.region}:${data.aws_caller_identity.main.account_id}:replicationgroup:integrates-*",
            "arn:aws:elasticache:${var.region}:${data.aws_caller_identity.main.account_id}:subnetgroup:integrates-*",
          ]
        },
        {
          Sid    = "elasticloadbalancingRead"
          Effect = "Allow"
          Action = [
            "elasticloadbalancing:Describe*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "s3Read"
          Effect = "Allow"
          Action = [
            "s3:Get*",
            "s3:ListBucket"
          ]
          Resource = [
            "arn:aws:s3:::continuous-data",
            "arn:aws:s3:::continuous-data/*",
            "arn:aws:s3:::continuous-repositories",
            "arn:aws:s3:::continuous-repositories/*",
            "arn:aws:s3:::skims.data",
            "arn:aws:s3:::skims.data/*",
          ]
        },
        {
          Sid    = "s3Write"
          Effect = "Allow"
          Action = ["*"]
          Resource = [
            "arn:aws:s3:::fluidattacks-terraform-states-prod/integrates*",
            "arn:aws:s3:::fluidintegrates*/*",
            "arn:aws:s3:::fluidintegrates*",
            "arn:aws:s3:::integrates*/*",
            "arn:aws:s3:::integrates*",
            "arn:aws:s3:::continuous*",
            "arn:aws:s3:::continuous*/*",
          ]
        },
        {
          Sid    = "batchRead"
          Effect = "Allow"
          Action = [
            "batch:Describe*",
            "batch:List*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "batchWrite"
          Effect = "Allow"
          Action = [
            "batch:CancelJob",
            "batch:SubmitJob",
            "batch:TerminateJob",
          ]
          Resource = [
            "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-definition/*",
            "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-queue/*",
          ]
        },
        {
          Sid    = "logsRead"
          Effect = "Allow"
          Action = [
            "logs:Describe*",
            "logs:Filter*",
            "logs:Get*",
            "logs:List*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "logsWrite"
          Effect = "Allow"
          Action = ["*"]
          Resource = [
            "arn:aws:logs:us-east-1:${data.aws_caller_identity.main.account_id}:log-group:FLUID*",
          ]
        },
        {
          Sid    = "logsGlobalWrite"
          Effect = "Allow"
          Action = [
            "logs:PutResourcePolicy",
          ]
          Resource = [
            "arn:aws:logs:us-east-1:${data.aws_caller_identity.main.account_id}:*",
          ]
        },
        {
          Sid    = "ec2Read"
          Effect = "Allow"
          Action = [
            "ec2:Describe*",
            "ec2:Get*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "ec2Write"
          Effect = "Allow"
          Action = [
            "ec2:RevokeSecurityGroupEgress",
            "ec2:RevokeSecurityGroupIngress",
            "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
            "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
            "ec2:ApplySecurityGroupsToClientVpnTargetNetwork",
            "ec2:AuthorizeSecurityGroupEgress",
            "ec2:AuthorizeSecurityGroupIngress",
            "ec2:CreateSecurityGroup",
            "ec2:DeleteSecurityGroup",
            "ec2:*Tags",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "eksRead"
          Effect = "Allow"
          Action = [
            "eks:Describe*",
            "eks:Get*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "eksWrite"
          Effect = "Allow"
          Action = ["*"]
          Resource = [
            "arn:aws:eks:${var.region}:${data.aws_caller_identity.main.account_id}:cluster/integrates-*"
          ]
        },
        {
          Sid      = "dynamoWrite"
          Effect   = "Allow"
          Action   = ["dynamodb:*"]
          Resource = ["*"]
        },
        {
          Sid    = "cloudwatchRead"
          Effect = "Allow"
          Action = [
            "cloudwatch:Describe*",
            "cloudwatch:Get*",
            "cloudwatch:List*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "backupWrite"
          Effect = "Allow"
          Action = [
            "backup:*",
            "backup-storage:*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "opensearchWrite"
          Effect = "Allow"
          Action = ["*"]
          Resource = [
            "arn:aws:es:${var.region}:${data.aws_caller_identity.main.account_id}:domain/integrates*"
          ]
        },
        {
          Sid    = "lambdaRead"
          Effect = "Allow"
          Action = [
            "lambda:Get*",
            "lambda:List*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "lambdaWrite"
          Effect = "Allow"
          Action = ["*"]
          Resource = [
            "arn:aws:lambda:${var.region}:${data.aws_caller_identity.main.account_id}:function:integrates*"
          ]
        },
        {
          Sid    = "lambdaGlobalWrite"
          Effect = "Allow"
          Action = [
            "lambda:CreateEventSourceMapping",
            "lambda:DeleteEventSourceMapping",
            "lambda:UpdateEventSourceMapping"
          ]
          Resource = ["*"]
        },
        {
          Sid    = "sqsAll"
          Effect = "Allow"
          Action = [
            "sqs:*",
            "sqs:ChangeMessageVisibility",
            "sqs:DeleteMessage",
            "sqs:GetQueueUrl",
            "sqs:ReceiveMessage",
          ]
          Resource = [
            "arn:aws:sqs:us-east-1:205810638802:skims-*",
            "arn:aws:sqs:us-east-1:205810638802:celery",
          ]
        },
      ]

      cloudflare = {
        accountZone = {
          effect = "allow"
          permission_groups = [
            data.cloudflare_api_token_permission_groups.all.permissions["Zone Read"],
            data.cloudflare_api_token_permission_groups.all.permissions["Cache Purge"],
            data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Write"],
            data.cloudflare_api_token_permission_groups.all.permissions["Firewall Services Write"],
            data.cloudflare_api_token_permission_groups.all.permissions["DNS Write"],
          ]
          resources = {
            "com.cloudflare.api.account.zone.*" = "*"
          }
        }
      }
    }

    keys = {
      prod_integrates = {
        admins = [
          "prod_common",
        ]
        users = [
          "prod_integrates",
        ]
        tags = {
          "Name"               = "prod_integrates"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_integrates_aws" {
  source = "./modules/aws"

  name   = "prod_integrates"
  policy = local.prod_integrates.policies.aws

  assume_role_policy = [
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
          ) : "system:serviceaccount:production:prod-integrates"
        },
      },
    },
  ]

  tags = {
    "Name"               = "prod_integrates"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

module "prod_integrates_keys" {
  source   = "./modules/key"
  for_each = local.prod_integrates.keys

  name   = each.key
  admins = each.value.admins
  users  = each.value.users
  tags   = each.value.tags
}

module "prod_integrates_publish_credentials" {
  source = "./modules/publish_credentials"

  providers = {
    gitlab = gitlab.universe
  }

  key_1     = module.prod_integrates_aws.keys.1
  key_2     = module.prod_integrates_aws.keys.2
  prefix    = "PROD_INTEGRATES"
  protected = true
}

module "prod_integrates_cloudflare" {
  source = "./modules/cloudflare"

  name   = "prod_integrates"
  policy = local.prod_integrates.policies.cloudflare
}
