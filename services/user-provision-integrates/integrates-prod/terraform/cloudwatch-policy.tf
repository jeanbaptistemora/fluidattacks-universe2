data "aws_iam_policy_document" "integrates-prod-cloudwatch-policy-data" {
  statement {
    effect  = "Allow"
    actions = ["cloudwatch:*"]
    resources = [
      "arn:aws:cloudwatch:${var.region}:${data.aws_caller_identity.current.account_id}:alarm:fi*",
      "arn:aws:cloudwatch::${data.aws_caller_identity.current.account_id}:dashboard/BinaryAlert"
    ]
  }
  statement {
    effect  = "Allow"
    actions = ["events:*"]
    resources = [
      "arn:aws:events:${var.region}:${data.aws_caller_identity.current.account_id}:rule/fi_binaryalert*"
    ]
  }
}

resource "aws_iam_policy" "integrates-prod-cloudwatch-policy" {
  description = "integrates-prod policy for cloudwatch"
  name        = "${var.user-name}-cloudwatch-actions-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-cloudwatch-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-cloudwatch-actions" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-cloudwatch-policy.arn
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-cloudwatch" {
  user       = var.user-name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}
