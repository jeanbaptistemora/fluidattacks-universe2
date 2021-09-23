data "aws_iam_policy_document" "sorts_prod_policy_data" {
  # S3 access to the terraform state
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod/sorts.tfstate",
    ]
  }

  # IAM and AWS SSO role
  statement {
    effect = "Allow"
    actions = [
      "iam:*",
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:instance-profile/sorts_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user_provision/sorts_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/sorts_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/sorts_*",
    ]
  }

  # DynamoDB for locking terraform state
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:DeleteItem",
      "dynamodb:GetItem",
      "dynamodb:PutItem",
    ]
    resources = [
      var.terraform_state_lock_arn,
    ]
  }

  # Batch access
  statement {
    effect  = "Allow"
    actions = ["batch:SubmitJob"]
    resources = [
      "arn:aws:batch:${var.region}:${data.aws_caller_identity.current.account_id}:job-definition/*",
      "arn:aws:batch:${var.region}:${data.aws_caller_identity.current.account_id}:job-queue/spot*",
      "arn:aws:batch:${var.region}:${data.aws_caller_identity.current.account_id}:job-queue/dedicated*",
    ]
  }
  statement {
    effect    = "Allow"
    actions   = ["batch:ListJobs"]
    resources = ["*"]
  }

  # S3 admin over Sorts bucket
  statement {
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::sorts",
      "arn:aws:s3:::sorts/*"
    ]
  }

  # SageMaker access
  statement {
    effect = "Allow"
    actions = [
      "sagemaker:*"
    ]
    resources = [
      "arn:aws:sagemaker:${var.region}:${data.aws_caller_identity.current.account_id}:training-job/sagemaker*",
      "arn:aws:sagemaker:${var.region}:${data.aws_caller_identity.current.account_id}:training-job/sorts*",
      "arn:aws:sagemaker:${var.region}:${data.aws_caller_identity.current.account_id}:hyper-parameter-tuning-job/sagemaker*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "sagemaker:List*",
    ]
    resources = ["*"]
  }

  # CloudWatch logs access
  statement {
    effect = "Allow"
    actions = [
      "logs:*"
    ]
    resources = [
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/sagemaker/TrainingJobs",
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/sagemaker/TrainingJobs:log-stream:*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "logs:DescribeLogGroups",
      "logs:GetLogEvents",
    ]
    resources = ["*"]
  }

  # Redshift
  statement {
    effect = "Allow"
    actions = [
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
      "kms:CreateKey",
      "kms:CreateAlias",
      "kms:Describe*",
      "kms:Encrypt",
      "kms:Get*",
      "kms:List*",
      "kms:PutKeyPolicy",
      "kms:TagResource",
      "kms:UntagResource",
      "kms:UpdateAlias",
    ]
    resources = [
      "*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/sorts*"
    ]
  }

  # Cost Management
  statement {
    effect = "Allow"
    actions = [
      "aws-portal:View*",
      "ce:Describe*",
      "ce:ListCostCategoryDefinitions",
      "cur:DescribeReportDefinitions",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "sorts_prod_policy" {
  description = "sorts_prod policy"
  name        = "sorts_prod_policy"
  path        = "/user_provision/"
  policy      = data.aws_iam_policy_document.sorts_prod_policy_data.json
}

resource "aws_iam_user_policy_attachment" "sorts_prod_attach_policy" {
  user       = "sorts_prod"
  policy_arn = aws_iam_policy.sorts_prod_policy.arn
}
