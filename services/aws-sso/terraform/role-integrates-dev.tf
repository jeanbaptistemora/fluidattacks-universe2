resource "aws_iam_role" "integrates-dev" {
  name = "integrates-dev"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json
}

resource "aws_iam_role_policy_attachment" "integrates-dev-push-cloudwatch" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-dynamo-full-access" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-cloudwatch-actions" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/integrates-dev-cloudwatch-actions-policy"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-lambda" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/integrates-dev-lambda-policy"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-cloudfront" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/integrates-dev-cloudfront-policy"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-user-provision" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/user-provision-policy-integrates-dev"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-iam" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/integrates-dev-iam-policy"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-sns" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/integrates-dev-sns-policy"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-ec2" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/integrates-dev-ec2-policy"
}

resource "aws_iam_role_policy_attachment" "integrates-dev-sqs" {
  role       = aws_iam_role.integrates-dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/integrates-dev-sqs-policy"
}
