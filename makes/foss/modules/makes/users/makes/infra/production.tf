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

# User

resource "aws_iam_user" "prod" {
  name = "serves-prod"
  path = "/user-provision/"

  tags = {
    "Name"            = "serves-prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_access_key" "prod-key-1" {
  user = "serves-prod"
}

resource "aws_iam_access_key" "prod-key-2" {
  user = "serves-prod"
}

module "publish_credentials_prod" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.prod-key-1
  key_2        = aws_iam_access_key.prod-key-2
  prefix       = "MAKES_PROD"
  protected    = true
}
