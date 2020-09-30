data "aws_iam_policy_document" "prod-policy-data" {

  # S3
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject",
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/observes-*",
      "arn:aws:s3:::continuous-repositories",
      "arn:aws:s3:::continuous-repositories/*",
      "arn:aws:s3:::fluidanalytics",
      "arn:aws:s3:::fluidanalytics/*"
    ]
  }

  # IAM
  statement {
    effect = "Allow"
    actions = [
      "iam:List*",
      "iam:Get*",
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["iam:*"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/observes-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/observes-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/analytics",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/analytics",
    ]
  }

  # Batch access
  statement {
    effect = "Allow"
    actions = ["batch:ListJobs"]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = ["batch:SubmitJob"]
    resources = [
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-definition/default",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/default",
    ]
  }

  # DynamoDB
  statement {
    effect  = "Allow"
    actions = [
      "dynamodb:*",
    ]
    resources = ["*"]
  }

  # Redshift
  statement {
    effect  = "Allow"
    actions = [
      "redshift:*",
    ]
    resources = [
      "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:cluster:fluid-redshift"
    ]
  }

  # KMS
  statement {
    effect = "Allow"
    actions = [
      "kms:UntagResource",
      "kms:TagResource",
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
      "kms:CreateKey",
      "kms:CreateAlias",
      "kms:UpdateAlias"
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["kms:*"]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/observes-*"
    ]
  }
}

resource "aws_iam_policy" "prod-policy" {
  description = "observes prod policy"
  name        = "observes-prod-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "prod-attach-policy" {
  user       = "observes-prod"
  policy_arn = aws_iam_policy.prod-policy.arn
}

resource "aws_iam_user" "prod" {
  name = "observes-prod"
  path = "/user-provision/"

  tags = {
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "prod-key-1" {
  user = "observes-prod"
}

resource "aws_iam_access_key" "prod-key-2" {
  user = "observes-prod"
}
