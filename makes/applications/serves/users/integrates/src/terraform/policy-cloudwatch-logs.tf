resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-cloudwatch-logs" {
  user       = "integrates-prod"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy-cloudwatch-logs" {
  user       = "integrates-dev"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}
