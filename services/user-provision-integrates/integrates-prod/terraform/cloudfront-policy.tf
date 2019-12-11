data "aws_iam_policy_document" "integrates-prod-cloudfront-policy-data" {
  statement {
    effect    = "Allow"
    actions   = ["cloudfront:*"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "integrates-prod-cloudfront-policy" {
  description = "integrates-prod policy for cloudfront"
  name        = "${var.user-name}-cloudfront-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-cloudfront-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-cloudfront" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-cloudfront-policy.arn
}
