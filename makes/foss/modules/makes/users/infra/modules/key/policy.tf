data "aws_caller_identity" "current" {}
locals {
  admin_arns = concat(
    ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"],
    [for user in var.admins : "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${user}"],
    [for user in var.admins : "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${user}"],
  )
  user_arns = concat(
    [for user in var.users : "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${user}"],
    [for user in var.users : "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${user}"],
  )
  policy = {
    Version = "2012-10-17",
    Statement = [
      {
        Sid      = "Key Administrators",
        Effect   = "Allow",
        Action   = ["kms:*"],
        Resource = "*",
        Principal = {
          AWS = local.admin_arns
        },
      },
      {
        Sid    = "Key Users",
        Effect = "Allow",
        Action = [
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:Encrypt",
          "kms:DescribeKey",
          "kms:Decrypt",
        ],
        Resource = "*",
        Principal = {
          AWS = concat(
            local.admin_arns,
            local.user_arns,
          )
        },
      },
      {
        Sid    = "Attachment Of Persistent Resources",
        Effect = "Allow",
        Action = [
          "kms:RevokeGrant",
          "kms:ListGrants",
          "kms:CreateGrant",
        ],
        Resource = "*",
        Principal = {
          AWS = concat(
            local.admin_arns,
            local.user_arns,
          )
        },
        Condition = {
          Bool = {
            "kms:GrantIsForAWSResource" = "true",
          },
        },
      },
    ],
  }
}
