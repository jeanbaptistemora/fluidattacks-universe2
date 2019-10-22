resource "aws_iam_role" "SSO_Finance" {
  name               = "SSO_Finance"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json
}
