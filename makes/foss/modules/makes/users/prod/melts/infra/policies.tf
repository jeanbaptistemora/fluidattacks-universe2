locals {
  aws = {
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "s3Write"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:s3:::fluidattacks-terraform-states-prod/melts*",
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
}
