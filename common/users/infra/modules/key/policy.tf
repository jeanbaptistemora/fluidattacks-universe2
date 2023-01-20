data "aws_caller_identity" "main" {}
locals {
  admin_arns = concat(
    ["arn:aws:iam::${data.aws_caller_identity.main.account_id}:root"],
    [for user in var.admins : "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/${user}"],
  )
  user_arns = [
    for user in var.users : "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/${user}"
  ]
  read_user_arns = [
    for user in var.read_users : "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/${user}"

  ]
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
        Sid    = "Key Write Users",
        Effect = "Allow",
        Action = [
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:Encrypt"
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
        Sid    = "Key Read Users",
        Effect = "Allow",
        Action = [
          "kms:DescribeKey",
          "kms:Decrypt",
        ],
        Resource = "*",
        Principal = {
          AWS = concat(
            local.admin_arns,
            local.read_user_arns,
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
