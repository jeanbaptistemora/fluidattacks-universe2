resource "aws_iam_role" "SSO" {
  name               = "SSO"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json
}
