data "aws_iam_policy_document" "skims_prod_policy_data" {
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
      "arn:aws:s3:::fluidattacks-terraform-states-prod/skims.tfstate",
    ]
  }

  # IAM and AWS SSO role
  statement {
    effect = "Allow"
    actions = [
      "iam:*",
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user_provision/skims_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/skims_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/skims_*",
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

resource "aws_iam_policy" "skims_prod_policy" {
  description = "skims_prod policy"
  name        = "${var.user_name}_policy"
  path        = "/user_provision/"
  policy      = data.aws_iam_policy_document.skims_prod_policy_data.json
}

resource "aws_iam_user_policy_attachment" "skims_prod_attach_policy" {
  user       = var.user_name
  policy_arn = aws_iam_policy.skims_prod_policy.arn
}
