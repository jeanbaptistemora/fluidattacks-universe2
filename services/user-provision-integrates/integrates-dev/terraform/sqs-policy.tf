data "aws_iam_policy_document" "integrates-dev-sqs-policy-data" {
  statement {
    effect    = "Allow"
    actions   = ["sqs:*"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "integrates-dev-sqs-policy" {
  description = "integrates-dev policy for sqs"
  name        = "${var.user-name}-sqs-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-dev-sqs-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy-sqs" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-dev-sqs-policy.arn
}
