data "aws_iam_policy_document" "integrates-prod-policy-data" {
  statement {
    effect    = "Allow"
    actions   = ["sqs:*"]
    resources = ["*"]
  }

  statement {
    effect  = "Allow"
    actions = ["sns:*"]
    resources = [
      "arn:aws:sns:${var.region}:${data.aws_caller_identity.current.account_id}:fi_binaryalert*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "application-autoscaling:RegisterScalableTarget",
      "application-autoscaling:PutScalingPolicy",
      "application-autoscaling:DescribeScalingPolicies",
      "application-autoscaling:DescribeScalingActivities",
      "application-autoscaling:DescribeScalableTargets",
      "application-autoscaling:DeregisterScalableTarget",
      "application-autoscaling:DeleteScalingPolicy"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "integrates-prod-policy" {
  description = "integrates-prod policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-policy.arn
}
