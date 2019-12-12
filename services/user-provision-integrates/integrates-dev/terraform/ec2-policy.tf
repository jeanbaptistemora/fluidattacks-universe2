data "aws_iam_policy_document" "integrates-dev-ec2-policy-data" {
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

resource "aws_iam_policy" "integrates-dev-ec2-policy" {
  description = "integrates-dev policy for ec2"
  name        = "${var.user-name}-ec2-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-dev-ec2-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy-ec2" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-dev-ec2-policy.arn
}
