resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy-cloudwatch-logs" {
  user       = var.user-name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}
