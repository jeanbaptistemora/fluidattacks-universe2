locals {
  aws = {
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "iamRead"
        Effect = "Allow"
        Action = [
          "iam:Get*",
          "iam:List*",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "s3Read"
        Effect = "Allow"
        Action = [
          "s3:Get*",
          "s3:List*",
        ]
        Resource = ["*"]
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
        Sid    = "kmsRead"
        Effect = "Allow"
        Action = [
          "kms:Describe*",
          "kms:Get*",
          "kms:List*",
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
        Resource = [
          "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock",
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
