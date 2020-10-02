resource "aws_iam_role" "asserts-prod" {
  name = "asserts-prod"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "asserts-prod"
    "management:type"    = "production"
    "management:product" = "asserts"
  }
}

resource "aws_iam_role_policy_attachment" "asserts-prod" {
  role       = aws_iam_role.asserts-prod.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/asserts-prod-policy"
}
