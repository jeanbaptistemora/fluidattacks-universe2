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
  name = "helpdesk"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json

  tags = {
    "management:type"    = "production"
    "management:product" = "serves"
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
