resource "aws_iam_role" "integrates-dev" {
  name = "integrates-dev"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-push-cloudwatch" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-dynamo-full-access" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "integrates-dev" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/integrates-dev-policy"
}
