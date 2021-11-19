locals {
  aws = {
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "read"
        Effect = "Allow"
        Action = [
          "application-autoscaling:Describe*",
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
          "eks:Describe*",
          "eks:Get*",
          "elasticache:Describe*",
          "elasticache:List*",
          "iam:Get*",
          "iam:List*",
          "kms:Describe*",
          "kms:Get*",
          "kms:List*",
          "lambda:Get*",
          "lambda:List*",
          "logs:Describe*",
          "logs:Get*",
          "logs:List*",
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
          "arn:aws:s3:::docs-dev.fluidattacks.com",
          "arn:aws:s3:::docs-dev.fluidattacks.com/*",
          "arn:aws:s3:::fluidintegrates.analytics/*atfluid",
          "arn:aws:s3:::fluidintegrates.analytics/*atfluid/*",
          "arn:aws:s3:::integrates.front.development.fluidattacks.com",
          "arn:aws:s3:::integrates.front.development.fluidattacks.com/*",
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
