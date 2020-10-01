data "aws_iam_policy_document" "erp-finance-policy-data" {
  statement {
    sid = "AllowStartAndStopInstance"
    effect = "Allow"
    actions = [
      "ec2:StartInstances",
      "ec2:StopInstances"
    ]
    resources = [
      "arn:aws:ec2:us-east-1:${data.aws_caller_identity.current.account_id}:instance/i-0ba149836e9bb8e7c"
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
  name = "finance"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json

  tags = {
    "Name"               = "finance"
    "management:type"    = "production"
    "management:product" = "serves"
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
