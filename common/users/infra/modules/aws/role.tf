# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

data "aws_caller_identity" "main" {}
locals {
  assume_role_policy = {
    Version = "2012-10-17",
    Statement = concat(
      [
        {
          Sid    = "ciAccessProd",
          Effect = "Allow",
          Principal = {
            Federated = "arn:aws:iam::${data.aws_caller_identity.main.account_id}:oidc-provider/gitlab.com",
          },
          Action = "sts:AssumeRoleWithWebIdentity",
          Condition = {
            StringEquals = {
              "gitlab.com:sub" : "project_path:fluidattacks/universe:ref_type:branch:ref:trunk"
            },
          },
        },
        {
          Sid    = "ecsTaskAccess",
          Effect = "Allow",
          Principal = {
            Service = [
              "ec2.amazonaws.com",
              "ecs-tasks.amazonaws.com",
            ],
          },
          Action = "sts:AssumeRole",
        },
        {
          Sid    = "oktaSAMLAccess",
          Effect = "Allow",
          Principal = {
            Federated = "arn:aws:iam::${data.aws_caller_identity.main.account_id}:saml-provider/okta-saml-provider",
          },
          Action = "sts:AssumeRoleWithSAML",
          Condition = {
            StringEquals = {
              "SAML:aud" = "https://signin.aws.amazon.com/saml",
            },
          },
        },
      ],
      var.assume_role_policy,
    )
  }
}

resource "aws_iam_role" "main" {
  name                 = var.name
  assume_role_policy   = jsonencode(local.assume_role_policy)
  max_session_duration = "32400"
  tags                 = var.tags
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}
