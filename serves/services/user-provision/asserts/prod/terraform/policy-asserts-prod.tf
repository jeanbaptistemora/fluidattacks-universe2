data "aws_iam_policy_document" "asserts-prod-policy-data" {

  # S3 state files and documentation
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-*",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/asserts-secret-management.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-*/user-provision-asserts-*.tfstate",
      "arn:aws:s3:::fluidattacks.com",
      "arn:aws:s3:::fluidattacks.com/resources/doc/asserts/*",
    ]
  }

  # IAM full permissions over owned users, roles and policies
  statement {
    effect  = "Allow"
    actions = [
      "iam:*"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/asserts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/asserts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/asserts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/asserts-*",
    ]
  }

  # KMS create Keys
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
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/asserts-*"
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

resource "aws_iam_policy" "asserts-prod-policy" {
  description = "asserts-prod policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.asserts-prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "asserts-prod-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.asserts-prod-policy.arn
}
