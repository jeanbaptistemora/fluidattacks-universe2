data "aws_iam_policy_document" "asserts-dev-policy-data" {

  # S3 state files
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-*",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/asserts-secret-management.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-*/user-provision-asserts-*.tfstate",
    ]
  }

  # IAM read over owned users, roles and policies
  statement {
    effect  = "Allow"
    actions = [
      "iam:GetUser",
      "iam:GetRole",
      "iam:GetPolicy",
      "iam:GetPolicyVersion",
      "iam:ListAttachedUserPolicies",
      "iam:ListAttachedRolePolicies"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/asserts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/asserts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/asserts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/asserts-*",
    ]
  }

  # KMS read keys
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

  # KMS full permissions
  statement {
    effect  = "Allow"
    actions = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/asserts-dev-*"
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

resource "aws_iam_policy" "asserts-dev-policy" {
  description = "asserts-dev policy"
  name        = "asserts-dev-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.asserts-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "asserts-dev-attach-policy" {
  user       = "asserts-dev"
  policy_arn = aws_iam_policy.asserts-dev-policy.arn
}
