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
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "athena:*",
        ],
        "Resource" : [
          aws_athena_database.monitoring.arn,
        ],
      },
      # For Redshift data source:
      # {
      #   "Effect" : "Allow",
      #   "Action" : [
      #     "redshift:DescribeClusters",
      #     "redshift:GetClusterCredentials",
      #     "redshift-data:*",
      #   ],
      #   "Resource" : [<observes-cluster>]
      # },
    ]
  })
}
