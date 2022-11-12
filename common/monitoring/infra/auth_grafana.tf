# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_iam_role" "grafana" {
  name = "common-monitoring-grafana"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "grafana.amazonaws.com"
        }
      },
    ]
  })
}


resource "aws_iam_role_policy_attachment" "grafana" {
  role       = aws_iam_role.grafana.name
  policy_arn = aws_iam_policy.grafana.arn
}

resource "aws_iam_policy" "grafana" {
  name = "common-monitoring-grafana"

  policy = jsonencode({
    "Version" = "2012-10-17",
    "Statement" = [
      {
        "Effect" = "Allow",
        "Action" = [
          "athena:ListDatabases",
          "athena:ListDataCatalogs",
          "athena:ListWorkGroups",
        ],
        "Resource" = "*",
      },
      {
        "Effect" = "Allow",
        "Action" = [
          "glue:GetDatabases"
        ],
        "Resource" = [
          "arn:aws:glue:*:*:catalog",
        ],
      },
      # For Redshift data source:
      # {
      #   "Effect" ="Allow",
      #   "Action" =[
      #     "redshift:DescribeClusters",
      #     "redshift:GetClusterCredentials",
      #     "redshift-data:*",
      #   ],
      #   "Resource" =[<observes-cluster>]
      # },
    ]
  })
}

resource "okta_app_saml" "grafana" {
  label             = "Grafana - Universe"
  preconfigured_app = "amazonmanagedgrafanasaml"

  app_settings_json = jsonencode({
    "nameSpace" = "g-41cb062f0f"
    "region"    = "us-east-1"
  })
  app_links_json = jsonencode({
    "amazonmanagedgrafanasaml_link" = true,
  })
  user_name_template      = "$${source.login}"
  user_name_template_type = "BUILT_IN"

  attribute_statements {
    type   = "EXPRESSION"
    name   = "role"
    values = ["admin"]
  }

  lifecycle {
    ignore_changes = [users]
  }
}


resource "okta_app_user" "grafana" {
  app_id   = okta_app_saml.grafana.id
  user_id  = "00ul9azo2c04YGZN2357"
  username = "kamado@fluidattacks.com"
}
