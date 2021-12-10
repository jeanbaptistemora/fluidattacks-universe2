locals {
  aws = {
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "s3Write"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:s3:::docs.fluidattacks.com",
          "arn:aws:s3:::docs.fluidattacks.com/*",
          "arn:aws:s3:::docs-dev.fluidattacks.com",
          "arn:aws:s3:::docs-dev.fluidattacks.com/*",
          "arn:aws:s3:::fluidattacks-terraform-states-prod/docs*",
        ]
      },
      {
        Sid    = "kmsRead"
        Effect = "Allow"
        Action = [
          "kms:CreateAlias",
          "kms:CreateKey",
          "kms:Describe*",
          "kms:Get*",
          "kms:List*",
          "kms:TagResource",
          "kms:UntagResource",
          "kms:UpdateAlias",
        ]
        Resource = ["*"]
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
