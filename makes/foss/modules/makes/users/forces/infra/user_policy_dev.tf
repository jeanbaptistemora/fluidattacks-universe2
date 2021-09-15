data "aws_iam_policy_document" "forces_dev_policy_data" {
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
      "arn:aws:s3:::fluidattacks-terraform-states-prod/break-build.tfstate",
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
      "kms:ListAliases",
    ]
    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:key/*",
    ]
    condition {
      test     = "StringLike"
      variable = "kms:RequestAlias"
      values = [
        "alias/forces-*",
        "alias/continuous-*",
      ]
    }
  }

}

resource "aws_iam_policy" "forces_dev_policy" {
  description = "forces_dev policy"
  name        = "forces_dev_policy"
  path        = "/user_provision/"
  policy      = data.aws_iam_policy_document.forces_dev_policy_data.json
}

resource "aws_iam_user_policy_attachment" "forces_dev_attach_policy" {
  user       = "forces_dev"
  policy_arn = aws_iam_policy.forces_dev_policy.arn
}
