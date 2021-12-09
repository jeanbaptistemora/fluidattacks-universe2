locals {
  aws = {
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "s3Write"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:s3:::fluidattacks.com",
          "arn:aws:s3:::fluidattacks.com/*",
          "arn:aws:s3:::fluidattacks-terraform-states-prod/airs.tfstate",
          "arn:aws:s3:::web.eph.fluidattacks.com",
          "arn:aws:s3:::web.eph.fluidattacks.com/*",
        ]
      },
      {
        Sid    = "kmsWrite"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/web-*",
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
