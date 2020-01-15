resource "aws_iam_role" "finance-role" {
  name = "finance"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json
}

resource "aws_iam_role_policy_attachment" "finance-role-erp" {
  role       = aws_iam_role.finance-role.name
  policy_arn = aws_iam_policy.erp-finance-policy.arn
}
