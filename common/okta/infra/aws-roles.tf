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


# Helpdesk

data "aws_iam_policy_document" "helpdesk-policy-data" {
  statement {
    effect = "Allow"
    actions = [
      "ec2:Describe*Instance*",
      "ec2:StartInstances",
      "ec2:StopInstances",
      "ec2:ApplySecurityGroupsToClientVpnTargetNetwork",
      "ec2:DescribeSecurityGroupReferences",
      "ec2:DescribeSecurityGroups",
      "ec2:DescribeStaleSecurityGroups",
      "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
      "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "helpdesk-policy" {
  name        = "helpdesk"
  path        = "/"
  description = "Policy for heldesk role"

  policy = data.aws_iam_policy_document.helpdesk-policy-data.json
}

resource "aws_iam_role" "helpdesk-role" {
  name               = "helpdesk"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json

  tags = {
    "Name"               = "helpdesk"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_iam_role_policy_attachment" "helpdesk-role" {
  role       = aws_iam_role.helpdesk-role.name
  policy_arn = aws_iam_policy.helpdesk-policy.arn
}

resource "aws_iam_role_policy_attachment" "helpdesk-policy" {
  role       = aws_iam_role.helpdesk-role.name
  policy_arn = aws_iam_policy.helpdesk-policy.arn
}
