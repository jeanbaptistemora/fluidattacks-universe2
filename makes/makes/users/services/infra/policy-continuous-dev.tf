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
      "arn:aws:s3:::fluidattacks-terraform-states-prod/break-build.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/services-*",
    ]
  }

  # S3 read over continuous buckets
  statement {
    sid    = "s3ContinuousRepositoriesRead"
    effect = "Allow"
    actions = [
      "s3:Get*",
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::continuous-*",
      "arn:aws:s3:::continuous-*/*",
    ]
  }

  # IAM read break-build and AWS SSO role
  statement {
    effect = "Allow"
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
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/burp-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/burp-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/burp-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/secure-notes*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/secure-notes*",
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
}

resource "aws_iam_policy" "continuous-dev-policy" {
  description = "continuous-dev policy"
  name        = "continuous-dev-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.continuous-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "continuous-dev-attach-policy" {
  user       = "continuous-dev"
  policy_arn = aws_iam_policy.continuous-dev-policy.arn
}
