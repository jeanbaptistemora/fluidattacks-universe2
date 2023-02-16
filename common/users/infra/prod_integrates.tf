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
            "iam:Describe*",
          ]
          Resource = ["*"]
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
          Sid    = "s3Create"
          Effect = "Allow"
          Action = [
            "s3:CreateBucket"
          ]
          Resource = ["arn:aws:s3:::*"]
        },
        {
          Sid    = "s3Read"
          Effect = "Allow"
          Action = [
            "s3:Get*",
            "s3:ListBucket",
          ]
          Resource = [
            "arn:aws:s3:::integrates/continuous-data",
            "arn:aws:s3:::integrates/continuous-data/*",
            "arn:aws:s3:::integrates/continuous-repositories",
            "arn:aws:s3:::integrates/continuous-repositories/*",
            "arn:aws:s3:::machine.data",
            "arn:aws:s3:::machine.data/*",
            "arn:aws:s3:::sorts",
            "arn:aws:s3:::sorts/*",
          ]
        },
        {
          Sid    = "s3ReadFluid"
          Effect = "Allow"
          Action = [
            "s3:ListBucket",
          ]
          Resource = [
            "arn:aws:s3:::fluidattacks.com",
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
            "arn:aws:s3:::machine.data/",
            "arn:aws:s3:::machine.data/*",
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
            "batch:TagResource",
            "batch:TerminateJob",
            "batch:UntagResource",
          ]
          Resource = [
            "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-definition/*",
            "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-queue/*",
            "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job/*",
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
          Sid    = "logsWriteMachine"
          Effect = "Allow"
          Action = ["*"]
          Resource = [
            "arn:aws:logs:us-east-1:${data.aws_caller_identity.main.account_id}:log-group:skims",
            "arn:aws:logs:us-east-1:${data.aws_caller_identity.main.account_id}:log-group:skims:log-stream:*",
          ]
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
          Sid    = "cloudwatchWrite"
          Effect = "Allow"
          Action = [
            "cloudwatch:PutMetricData",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "cloudMachineLogs"
          Effect = "Allow"
          Action = [
            "logs:*",
          ]
          Resource = ["arn:aws:logs:${var.region}:${data.aws_caller_identity.main.account_id}:log-group:skims:log-stream:*"]
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
          Sid    = "opensearchRead"
          Effect = "Allow"
          Action = [
            "es:Describe*",
            "es:Get*",
            "es:List*",
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
          Sid    = "sqsWrite"
          Effect = "Allow"
          Action = [
            "sqs:CreateQueue",
            "sqs:DeleteQueue",
            "sqs:GetQueueAttributes",
            "sqs:SetQueueAttributes",
            "sqs:TagQueue",
            "sqs:UntagQueue",
            "sqs:AddPermission",
            "sqs:RemovePermission",
            "sqs:ListQueues",
          ]
          Resource = [
            "*",
          ]
        },
        {
          Sid    = "sqsAll"
          Effect = "Allow"
          Action = [
            "sqs:*",
            "sqs:ChangeMessageVisibility",
            "sqs:DeleteMessage",
            "sqs:GetQueueUrl",
            "sqs:PurgeQueue",
            "sqs:ReceiveMessage",
            "sqs:SendMessage",
          ]
          Resource = [
            "arn:aws:sqs:us-east-1:205810638802:skims-*",
            "arn:aws:sqs:us-east-1:205810638802:celery",
          ]
        },
        {
          Sid    = "XRay"
          Effect = "Allow"
          Action = [
            "PutTelemetryRecords",
            "PutTraceSegments"
          ]
          Resource = ["*"]
        }
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
        read_users = []
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

  name       = each.key
  admins     = each.value.admins
  read_users = each.value.read_users
  users      = each.value.users
  tags       = each.value.tags
}

module "prod_integrates_cloudflare" {
  source = "./modules/cloudflare"

  name   = "prod_integrates"
  policy = local.prod_integrates.policies.cloudflare
}
