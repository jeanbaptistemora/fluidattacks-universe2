data "aws_iam_policy_document" "integrates-dev-cloudfront-policy-data" {
  statement {
    effect    = "Allow"
    actions   = ["cloudfront:*"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "integrates-dev-cloudfront-policy" {
  description = "integrates-prod policy for cloudfront"
  name        = "${var.user-name}-cloudfront-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-dev-cloudfront-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy-cloudfront" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-dev-cloudfront-policy.arn
}
