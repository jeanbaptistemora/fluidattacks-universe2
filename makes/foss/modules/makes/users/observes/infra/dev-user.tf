data "aws_iam_policy_document" "dev-policy-data" {

  # S3
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:Get*"
    ]
    resources = [
      "arn:aws:s3:::observes.*"
    ]
  }
  # IAM
  statement {
    effect = "Allow"
    actions = [
      "iam:List*",
      "iam:Get*"
    ]
    resources = ["*"]
  }

  # DynamoDB
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:Describe*",
      "dynamodb:List*",
    ]
    resources = [
      "*"
    ]
  }

  # Batch
  statement {
    effect = "Allow"
    actions = [
      "batch:DescribeComputeEnvironments",
      "batch:DescribeJobs",
      "batch:DescribeJobDefinitions",
      "batch:DescribeJobQueues",
      "batch:ListJobs",
    ]
    resources = ["*"]
  }

  # CloudWatch
  statement {
    effect = "Allow"
    actions = [
      "logs:GetLogEvents",
      "logs:DescribeLogGroups",
    ]
    resources = [
      "arn:aws:logs:us-east-1:${data.aws_caller_identity.current.account_id}:log-group:/aws/batch/job:log-stream:*",
    ]
  }

  # Redshift
  statement {
    effect = "Allow"
    actions = [
      "redshift:Describe*",
      "redshift:List*",
      "redshift:View*",
      "redshift:Fetch*",
    ]
    resources = ["*"]
  }

  # KMS
  statement {
    effect = "Allow"
    actions = [
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "dev-policy" {
  description = "observes dev policy"
  name        = "observes-dev-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "dev-attach-policy" {
  user       = "observes-dev"
  policy_arn = aws_iam_policy.dev-policy.arn
}

resource "aws_iam_user" "dev" {
  name = "observes-dev"
  path = "/user-provision/"

  tags = {
    "Name"               = "observes-dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "dev-key-1" {
  user = "observes-dev"
}

resource "aws_iam_access_key" "dev-key-2" {
  user = "observes-dev"
}

module "publish_credentials_dev" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.dev-key-1
  key_2        = aws_iam_access_key.dev-key-2
  prefix       = "OBSERVES_DEV"
  protected    = false
}
