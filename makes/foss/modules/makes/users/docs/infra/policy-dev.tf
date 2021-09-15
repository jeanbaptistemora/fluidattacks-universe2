data "aws_iam_policy_document" "dev" {

  # S3 prod bucket
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:Get*",
    ]
    resources = [
      "arn:aws:s3:::docs.fluidattacks.com/*",
      "arn:aws:s3:::docs.fluidattacks.com",
    ]
  }

  # S3 ephemeral bucket
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:Get*",
      "s3:PutObject",
      "s3:PutObjectAcl",
      "s3:DeleteObject*",
    ]
    resources = [
      "arn:aws:s3:::docs-dev.fluidattacks.com/*",
      "arn:aws:s3:::docs-dev.fluidattacks.com",
    ]
  }

  # S3 state files
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod/docs*",
    ]
  }

  # IAM read over owned users, roles and policies
  statement {
    effect = "Allow"
    actions = [
      "iam:GetUser",
      "iam:GetRole",
      "iam:GetPolicy",
      "iam:GetPolicyVersion",
      "iam:ListAttachedUserPolicies",
      "iam:ListAttachedRolePolicies"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/docs*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/docs*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/docs*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/docs*",
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
    effect = "Allow"
    actions = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/docs*"
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

resource "aws_iam_policy" "dev" {
  name   = "docs_dev"
  path   = "/user-provision/"
  policy = data.aws_iam_policy_document.dev.json
}

resource "aws_iam_user_policy_attachment" "dev" {
  user       = "docs_dev"
  policy_arn = aws_iam_policy.dev.arn
}
