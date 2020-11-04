data "aws_iam_policy_document" "continuous-prod-policy-data" {

  # S3 read and write prod continuous-secret-management tfstate
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/continuous-secret-management.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/break-build.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/services-*",
    ]
  }

  # S3 Break Build
  statement {
    sid = "s3BreakBuildAdmin"
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::break-build-logs",
      "arn:aws:s3:::break-build-logs/*"
    ]
  }

  # S3 admin over continuous buckets
  statement {
    sid = "s3ContinuousRepositoriesAdmin"
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::continuous-*",
      "arn:aws:s3:::continuous-*/*"
    ]
  }

  # ECR Auth Token
  statement {
      sid = "ecrBreakBuildAdminAuthToken"
      effect = "Allow"
      actions = [
        "ecr:GetAuthorizationToken"
      ]
      resources = [
        "*"
      ]
  }

  # ECR Break Build
  statement {
    sid = "ecrBreakBuildAdmin"
    effect = "Allow"
    actions = [
      "ecr:*"
    ]
    resources = [
      "arn:aws:ecr:${var.region}:${data.aws_caller_identity.current.account_id}:repository/break-build-*"
    ]
  }

  # IAM Break Build and AWS SSO role
  statement {
    effect  = "Allow"
    actions = [
      "iam:*"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/continuous-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/continuous-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/continuous-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/continuous-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/asserts/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/asserts/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/burp-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/burp-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/burp-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/secure-notes*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/secure-notes*",
    ]
  }

  # KMS Create Keys
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

  # KMS FUll permissions over owned KMS keys
  statement {
    effect  = "Allow"
    actions = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/continuous-*"
    ]
  }

  # Sagemaker for sorts
  statement {
    effect  = "Allow"
    actions = [
      "sagemaker:*"
    ]
    resources = [
      "*"
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

  # Secretsmanager for forces
  statement {
    effect  = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:CreateSecret",
      "secretsmanager:DeleteSecret",
      "secretsmanager:DescribeSecret",
      "secretsmanager:GetResourcePolicy",
      "secretsmanager:PutSecretValue",
      "secretsmanager:RestoreSecret",
      "secretsmanager:UpdateSecret",
    ]
    resources = [
      "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:forces-*"
    ]
  }
}

resource "aws_iam_policy" "continuous-prod-policy" {
  description = "continuous-prod policy"
  name        = "continuous-prod-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.continuous-prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "continuous-prod-attach-policy" {
  user       = "continuous-prod"
  policy_arn = aws_iam_policy.continuous-prod-policy.arn
}
