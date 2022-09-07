# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

locals {
  policy = {
    Version = "2012-10-17",
    Statement = concat(
      [
        {
          Sid    = "PassSelf"
          Effect = "Allow"
          Action = ["iam:PassRole"]
          Resource = [
            aws_iam_role.main.arn
          ]
        },
      ],
      var.policy,
    )
  }
}

resource "aws_iam_policy" "main" {
  name   = var.name
  policy = jsonencode(local.policy)
  tags   = var.tags
}
