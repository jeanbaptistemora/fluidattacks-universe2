resource "aws_iam_role" "integrates-dev" {
  name                 = "integrates-dev"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "integrates-dev"
    "management:type"    = "development"
    "management:product" = "integrates"
  }
}

resource "aws_iam_role_policy_attachment" "integrates-dev-push-cloudwatch" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = module.external.aws_iam_policies["cloudwatch-push"].arn
}

resource "aws_iam_role_policy_attachment" "integrates-dev-dynamo-full-access" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = module.external.aws_iam_policies["dynamodb-admin"].arn
}

resource "aws_iam_role_policy_attachment" "integrates-dev" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = module.external.aws_iam_policies["integrates-dev-policy"].arn
}
