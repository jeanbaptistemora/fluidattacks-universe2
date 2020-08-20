data "aws_iam_policy_document" "prod-policy-data" {

  statement {
    effect  = "Allow"
    actions = [
      "sns:*",
      "rds:*",
      "s3:*",
      "dynamodb:*",
      "elasticloadbalancing:*",
      "autoscaling:*",
      "sqs:*",
      "iam:*",
      "secretsmanager:*",
      "cloudwatch:*",
      "kms:*",
      "lambda:*",
      "route53:*",
      "ec2:*",
      "ecr:*",
      "eks:*",
      "elasticache:*",
      "acm:*",
      "events:*",
      "logs:*"
    ]
    resources = ["*"]
  }

}

resource "aws_iam_policy" "prod-policy" {
  description = "serves prod policy"
  name        = "serves-prod-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "prod-attach-policy" {
  user       = "serves-prod"
  policy_arn = aws_iam_policy.prod-policy.arn
}
