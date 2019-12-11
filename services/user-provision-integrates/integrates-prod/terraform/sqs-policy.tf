data "aws_iam_policy_document" "integrates-prod-sqs-policy-data" {
  statement {
    effect    = "Allow"
    actions   = ["sqs:*"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "integrates-prod-sqs-policy" {
  description = "integrates-prod policy for sqs"
  name        = "${var.user-name}-sqs-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-sqs-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-sqs" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-sqs-policy.arn
}
