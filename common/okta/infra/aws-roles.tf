# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# Finance

data "aws_iam_policy_document" "erp-finance-policy-data" {
  statement {
    sid    = "AllowStartAndStopInstance"
    effect = "Allow"
    actions = [
      "ec2:StartInstances",
      "ec2:StopInstances"
    ]
    resources = [
      "arn:aws:ec2:us-east-1:${data.aws_caller_identity.current.account_id}:instance/i-025095ae174dfaa99"
    ]
  }
}

resource "aws_iam_policy" "erp-finance-policy" {
  name        = "erp-finance"
  path        = "/"
  description = "Policy for turning on and off the erp machine"

  policy = data.aws_iam_policy_document.erp-finance-policy-data.json
}

resource "aws_iam_role" "finance-role" {
  name               = "finance"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json

  tags = {
    "Name"               = "finance"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_iam_role_policy_attachment" "finance-role-erp" {
  role       = aws_iam_role.finance-role.name
  policy_arn = aws_iam_policy.erp-finance-policy.arn
}

resource "aws_iam_role_policy_attachment" "finance-role-read-ec2" {
  role       = aws_iam_role.finance-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}
