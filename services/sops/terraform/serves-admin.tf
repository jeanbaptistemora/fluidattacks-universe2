data "aws_iam_policy_document" "serves-admin-data" {

  statement {
    sid = "General admin"
    effect = "Allow"
    actions = [
      "sns:*",
      "rds:*",
      "s3:*",
      "dynamodb:Scan",
      "elasticloadbalancing:*",
      "autoscaling:*",
      "iam:*",
      "secretsmanager:*",
      "cloudwatch:*",
      "kms:*",
      "route53:*",
      "ecr:*",
      "ec2:*",
      "eks:*",
      "elasticache:*"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "serves-admin" {
  name        = "serves-admin"
  path        = "/serves/"
  description = "Policy for serves administration"

  policy = data.aws_iam_policy_document.serves-admin-data.json
}

resource "aws_iam_group" "serves-admin" {
  name = "serves-admin"
  path = "/serves/"
}

resource "aws_iam_policy_attachment" "serves-admin" {
  name       = "serves-admin"
  groups     = [aws_iam_group.serves-admin.name]
  policy_arn = aws_iam_policy.serves-admin.arn
}
