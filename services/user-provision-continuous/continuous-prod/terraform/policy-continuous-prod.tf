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
      "arn:aws:s3:::fluidattacks-terraform-states-prod/break-build.tfstate"
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
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/continuous-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/asserts/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/asserts/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/break-build-*"
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
}

resource "aws_iam_policy" "continuous-prod-policy" {
  description = "continuous-prod policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.continuous-prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "continuous-prod-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.continuous-prod-policy.arn
}
