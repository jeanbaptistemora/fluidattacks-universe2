resource "aws_iam_role" "web-admin" {
  name                 = "web-admin"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"
}

resource "aws_iam_role_policy_attachment" "attach-break-build-audit-policy" {
  role       = aws_iam_role.web-admin.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/web-prod-policy"
}
