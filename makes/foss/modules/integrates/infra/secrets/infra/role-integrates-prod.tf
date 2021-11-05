resource "aws_iam_role" "integrates-prod" {
  name                 = "integrates-prod"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"            = "integrates-prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_role_policy_attachment" "integrates-prod-push-cloudwatch" {
  role       = aws_iam_role.integrates-prod.name
  policy_arn = module.external.aws_iam_policies["cloudwatch-push"].arn
}

resource "aws_iam_role_policy_attachment" "integrates-prod-dynamo-full-access" {
  role       = aws_iam_role.integrates-prod.name
  policy_arn = module.external.aws_iam_policies["dynamodb-admin"].arn
}

resource "aws_iam_role_policy_attachment" "integrates-prod" {
  role       = aws_iam_role.integrates-prod.name
  policy_arn = module.external.aws_iam_policies["integrates-prod-policy"].arn
}
