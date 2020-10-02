resource "aws_iam_role" "integrates-prod" {
  name = "integrates-prod"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "integrates-prod"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_iam_role_policy_attachment" "integrates-prod-push-cloudwatch" {
  role       = aws_iam_role.integrates-prod.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_iam_role_policy_attachment" "integrates-prod-dynamo-full-access" {
  role       = aws_iam_role.integrates-prod.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "integrates-prod" {
  role       = aws_iam_role.integrates-prod.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/integrates-prod-policy"
}
