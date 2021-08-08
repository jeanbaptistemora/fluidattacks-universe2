data "aws_iam_policy_document" "sorts_dev_policy_data" {
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
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod/sorts.tfstate",
    ]
  }

  # IAM and AWS SSO role
  statement {
    effect = "Allow"
    actions = [
      "iam:GetInstanceProfile",
      "iam:GetUser",
      "iam:GetRole",
      "iam:GetPolicy",
      "iam:GetPolicyVersion",
      "iam:ListAccessKeys",
      "iam:ListAttachedUserPolicies",
      "iam:ListAttachedRolePolicies",
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

  # KMS
  statement {
    effect = "Allow"
    actions = [
      "kms:Describe*",
      "kms:Get*",
      "kms:List*"
    ]
    resources = [
      "*"
    ]
  }

  # S3 access to Sorts bucket
  statement {
    effect = "Allow"
    actions = [
      "s3:Get*",
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::sorts",
      "arn:aws:s3:::sorts/*"
    ]
  }
}

resource "aws_iam_policy" "sorts_dev_policy" {
  description = "sorts_dev policy"
  name        = "sorts_dev_policy"
  path        = "/user_provision/"
  policy      = data.aws_iam_policy_document.sorts_dev_policy_data.json
}

resource "aws_iam_user_policy_attachment" "sorts_dev_attach_policy" {
  user       = "sorts_dev"
  policy_arn = aws_iam_policy.sorts_dev_policy.arn
}
