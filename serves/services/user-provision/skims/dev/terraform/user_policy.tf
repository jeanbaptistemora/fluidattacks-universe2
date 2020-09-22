data "aws_iam_policy_document" "skims_dev_policy_data" {
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
      "arn:aws:s3:::fluidattacks-terraform-states-prod/skims.tfstate",
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
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:instance-profile/skims_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user_provision/skims_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/skims_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/skims_*",
    ]
  }

  # EC2
  statement {
    effect = "Allow"
    actions = [
      "ec2:Describe*",
    ]
    resources = ["*"]
  }

  # KMS
  statement {
    effect = "Allow"
    actions = [
      "kms:Describe*",
      "kms:Get*",
      "kms:List*",
    ]
    resources = [
      "*"
    ]
  }

  # S3 access to skims buckets
  statement {
    effect = "Allow"
    actions = [
      "s3:Get*",
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::skims.*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:Put*",
    ]
    resources = [
      "arn:aws:s3:::skims.data/dependencies/*"
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

resource "aws_iam_policy" "skims_dev_policy" {
  description = "skims_dev policy"
  name        = "${var.user_name}_policy"
  path        = "/user_provision/"
  policy      = data.aws_iam_policy_document.skims_dev_policy_data.json
}

resource "aws_iam_user_policy_attachment" "skims_dev_attach_policy" {
  user       = var.user_name
  policy_arn = aws_iam_policy.skims_dev_policy.arn
}
