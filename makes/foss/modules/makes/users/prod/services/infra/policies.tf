locals {
  aws = {
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "generalRead"
        Effect = "Allow"
        Action = [
          "iam:Get*",
          "iam:List*",
          "kms:CreateAlias",
          "kms:CreateKey",
          "kms:Describe*",
          "kms:Get*",
          "kms:List*",
          "kms:TagResource",
          "kms:UntagResource",
          "kms:UpdateAlias",
          "s3:Get*",
          "s3:List*",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "generalWrite"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/continuous*",
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/secure-notes*",
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/continuous*",
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/continuous*",
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/secure-notes*",
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/continuous*",
          "arn:aws:s3:::continuous*",
          "arn:aws:s3:::fluidattacks-terraform-states-prod/break*",
          "arn:aws:s3:::fluidattacks-terraform-states-prod/continuous*",
          "arn:aws:s3:::fluidattacks-terraform-states-prod/services*",
        ]
      },
      {
        Sid    = "sagemakerWrite"
        Effect = "Allow"
        Action = [
          "sagemaker:*",
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
