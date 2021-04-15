resource "aws_iam_role" "docs_dev" {
  name                 = "docs_dev"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "docs_dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "docs_dev" {
  role       = aws_iam_role.docs_dev.name
  policy_arn = "arn:aws:iam::205810638802:policy/user-provision/docs_dev"
}
