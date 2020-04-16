data "aws_iam_policy_document" "continuous-dev-policy-data" {

  # S3 read continuous prod tfstates
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/continuous-secret-management.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/break-build.tfstate"
    ]
  }

  # S3 read break-build-logs bucket configs
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:Get*"
    ]
    resources = [
      "arn:aws:s3:::break-build-logs"
    ]
  }

  # S3 read continuoustest bucket continuous-repositories
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::continuous-repositories/continuoustest"
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

  # ECR read break-build
  statement {
    sid = "ecrBreakBuildAdmin"
    effect = "Allow"
    actions = [
      "ecr:DescribeRepositories",
      "ecr:ListTagsForResource",
      "ecr:GetLifecyclePolicy"
      ]
    resources = [
      "arn:aws:ecr:${var.region}:${data.aws_caller_identity.current.account_id}:repository/break-build-*"
    ]
  }

  # IAM read break-build and AWS SSO role
  statement {
    effect  = "Allow"
    actions = [
      "iam:GetUser",
      "iam:GetRole",
      "iam:GetPolicy",
      "iam:GetPolicyVersion",
      "iam:ListAccessKeys",
      "iam:ListAttachedUserPolicies",
      "iam:ListAttachedRolePolicies"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/continuous-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/continuous-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/continuous-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/continuous-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/asserts/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/asserts/break-build-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/break-build-*"
    ]
  }

  # KMS
  statement {
    effect = "Allow"
    actions = [
      "kms:List*",
      "kms:Get*",
      "kms:Describe*"
    ]
    resources = [
      "*"
    ]
  }

  # KMS FUll permissions over owned KMS keys
  statement {
    effect  = "Allow"
    actions = ["kms:*"]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/continuous-dev-*"
    ]
  }

  # DynamoDB
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:Describe*",
      "dynamodb:List*"
    ]
    resources = [
      "arn:aws:dynamodb:${var.region}:${data.aws_caller_identity.current.account_id}:table/bb_*",
    ]
  }
}

resource "aws_iam_policy" "continuous-dev-policy" {
  description = "continuous-dev policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.continuous-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "continuous-dev-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.continuous-dev-policy.arn
}
