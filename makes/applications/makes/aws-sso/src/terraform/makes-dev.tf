resource "aws_iam_role" "makes-dev-role" {
  name                 = "makes-dev"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "makes-dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "makes-dev" {
  role       = aws_iam_role.makes-dev-role.name
  policy_arn = "arn:aws:iam::205810638802:policy/user-provision/serves-dev-policy"
}
