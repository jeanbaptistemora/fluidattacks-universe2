data "aws_iam_policy_document" "okta-saml-policy-data" {
  statement {
    sid = "AllowListAliasesAndRoles"
    effect = "Allow"
    actions = [
      "iam:ListAccountAliases",
      "iam:ListRoles",
    ]
    resources = [
      "*",
    ]
  }
}

resource "aws_iam_user" "okta-access-user" {
  name = "okta-access-user"
  path = "/"
}

resource "aws_iam_policy" "okta-saml-policy" {
  name        = "okta-access"
  path        = "/"
  description = "Policy for allowing okta to list account aliases and roles"
  policy = data.aws_iam_policy_document.okta-saml-policy-data.json
}

resource "aws_iam_user_policy_attachment" "okta-access-user-attach-policy" {
  user       = aws_iam_user.okta-access-user.name
  policy_arn = aws_iam_policy.okta-saml-policy.arn
}
