# Policy

data "aws_iam_policy_document" "prod-policy-data" {

  statement {
    effect = "Allow"
    actions = [
      "access-analyzer:*",
      "batch:*",
      "budgets:*",
      "sns:*",
      "rds:*",
      "s3:*",
      "aws-portal:*",
      "ce:*",
      "cur:*",
      "savingsplans:*",
      "dynamodb:*",
      "elasticloadbalancing:*",
      "autoscaling:*",
      "sqs:*",
      "sts:*",
      "iam:*",
      "secretsmanager:*",
      "cloudwatch:*",
      "kms:*",
      "lambda:*",
      "route53:*",
      "ec2:*",
      "pricing:*",
      "ecr:*",
      "ecs:*",
      "eks:*",
      "elasticache:*",
      "acm:*",
      "events:*",
      "logs:*",
      "ssm:*",
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
