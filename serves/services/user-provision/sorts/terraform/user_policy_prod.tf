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
    effect = "Allow"
    actions = ["batch:SubmitJob"]
    resources = [
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-definition/default",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/default",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/default-uninterruptible"
    ]
  }
  statement {
    effect = "Allow"
    actions = ["batch:ListJobs"]
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
      "sagemaker:AddTags",
      "sagemaker:CreateTrainingJob",
      "sagemaker:DeleteTags",
      "sagemaker:DescribeTrainingJob",
      "sagemaker:ListTrainingJobs",
      "sagemaker:StopTrainingJob"
    ]
    resources = [
      "arn:aws:sagemaker:us-east-1:${data.aws_caller_identity.current.account_id}:training-job/sorts*"
    ]
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
