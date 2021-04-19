# Development

resource "aws_iam_role" "airs_dev" {
  name                 = "airs_dev"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "airs_dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "airs_dev" {
  role       = aws_iam_role.airs_dev.name
  policy_arn = "arn:aws:iam::205810638802:policy/user-provision/web-dev-policy"
}


# Production

resource "aws_iam_role" "airs_prod" {
  name                 = "airs_prod"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "airs_prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "airs_prod" {
  role       = aws_iam_role.airs_prod.name
  policy_arn = "arn:aws:iam::205810638802:policy/user-provision/web-prod-policy"
}
