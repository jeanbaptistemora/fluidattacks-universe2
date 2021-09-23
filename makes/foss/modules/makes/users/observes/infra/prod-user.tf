data "aws_iam_policy_document" "prod-policy-data" {

  # S3
  statement {
    effect = "Allow"
    actions = [
      "s3:DeleteObject",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:PutObject",
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
  statement {
    effect = "Allow"
    actions = [
      "s3:CreateBucket",
      "s3:DeleteBucket",
      "s3:DeleteObject",
      "s3:Get*",
      "s3:ListBucket",
      "s3:ListBucketVersions",
      "s3:Put*",
    ]
    resources = [
      "arn:aws:s3:::observes.*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:ListAllMyBuckets",
    ]
    resources = [
      "arn:aws:s3:::*"
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
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/analytics/analytics",
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
  statement {
    effect  = "Allow"
    actions = ["batch:SubmitJob"]
    resources = [
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-definition/*",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/dedicated*",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/observes*",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/spot*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "batch:CancelJob",
      "batch:TerminateJob",
    ]
    resources = [
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job/*",
    ]
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

  # DynamoDB
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:*",
    ]
    resources = ["*"]
  }

  # Redshift
  statement {
    effect = "Allow"
    actions = [
      "cloudwatch:*",
      "redshift:*",
      "redshift-data:*",
    ]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "redshift:*",
    ]
    resources = [
      "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:cluster:fluid-redshift",
      "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:dbname:fluid-redshift/*",
      "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:dbuser:fluid-redshift/*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "redshift:DescribeClusters",
      "redshift:DescribeClusterSubnetGroups",
      "redshift:DescribeEvents",
    ]
    resources = [
      "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:cluster:*",
      "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:event:*",
      "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:subnetgroup:*",
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
    "Name"               = "observes-prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "prod-key-1" {
  user = "observes-prod"
}

resource "aws_iam_access_key" "prod-key-2" {
  user = "observes-prod"
}

module "publish_credentials_prod" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.prod-key-1
  key_2        = aws_iam_access_key.prod-key-2
  prefix       = "OBSERVES_PROD"
  protected    = true
}
