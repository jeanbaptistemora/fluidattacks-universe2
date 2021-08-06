# Policy

data "aws_iam_policy_document" "dev-policy-data" {

  statement {
    effect = "Allow"
    actions = [
      "autoscaling:Describe*",
      "autoscaling:Get*",
      "access-analyzer:List*",
      "access-analyzer:Get*",
      "access-analyzer:Validate*",
      "batch:Describe*",
      "batch:Get*",
      "s3:List*",
      "s3:Get*",
      "iam:List*",
      "iam:Get*",
      "route53:List*",
      "route53:Get*",
      "acm:Describe*",
      "acm:List*",
      "lambda:Get*",
      "lambda:List*",
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
      "dynamodb:Describe*",
      "dynamodb:List*",
      "events:Describe*",
      "events:List*",
      "elasticloadbalancing:Describe*",
      "cloudwatch:List*",
      "cloudwatch:Describe*",
      "ec2:Describe*",
      "ec2:Get*",
      "eks:Describe*",
      "eks:List*",
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "dev-policy" {
  description = "serves dev policy"
  name        = "serves-dev-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "dev-attach-policy" {
  user       = "serves-dev"
  policy_arn = aws_iam_policy.dev-policy.arn
}


# User

resource "aws_iam_user" "dev" {
  name = "serves-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "serves-dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "dev-key-1" {
  user = "serves-dev"
}

resource "aws_iam_access_key" "dev-key-2" {
  user = "serves-dev"
}


# Outputs

output "dev-secret-key-id-1" {
  sensitive = true
  value     = aws_iam_access_key.dev-key-1.id
}

output "dev-secret-key-1" {
  sensitive = true
  value     = aws_iam_access_key.dev-key-1.secret
}

output "dev-secret-key-id-2" {
  sensitive = true
  value     = aws_iam_access_key.dev-key-2.id
}

output "dev-secret-key-2" {
  sensitive = true
  value     = aws_iam_access_key.dev-key-2.secret
}
