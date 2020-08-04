data "aws_iam_policy_document" "serves-prod-policy-data" {

  # S3 serves prod and ephemeral buckets
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
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "serves-prod-policy" {
  description = "serves-prod policy"
  name        = "serves-prod-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.serves-prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "serves-prod-attach-policy" {
  user       = "serves-prod"
  policy_arn = aws_iam_policy.serves-prod-policy.arn
}
