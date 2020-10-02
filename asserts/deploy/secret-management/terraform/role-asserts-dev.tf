resource "aws_iam_role" "asserts-dev" {
  name = "asserts-dev"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "asserts-dev"
    "management:type"    = "development"
    "management:product" = "asserts"
  }
}

resource "aws_iam_role_policy_attachment" "asserts-dev" {
  role       = aws_iam_role.asserts-dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/asserts-dev-policy"
}
