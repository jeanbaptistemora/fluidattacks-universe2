data "aws_iam_policy_document" "integrates-prod-sns-policy-data" {
  statement {
    effect  = "Allow"
    actions = ["sns:*"]
    resources = [
      "arn:aws:sns:${var.region}:${data.aws_caller_identity.current.account_id}:fi_binaryalert*"
    ]
  }
}

resource "aws_iam_policy" "integrates-prod-sns-policy" {
  description = "integrates-prod policy for sns"
  name        = "${var.user-name}-sns-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-sns-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-sns" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-sns-policy.arn
}
