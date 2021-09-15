data "aws_iam_policy_document" "forces_prod_policy_data" {
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
    effect = "Allow"
    actions = [
      "kms:*",
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

resource "aws_iam_policy" "forces_prod_policy" {
  description = "forces_prod policy"
  name        = "forces_prod_policy"
  path        = "/user_provision/"
  policy      = data.aws_iam_policy_document.forces_prod_policy_data.json
}

resource "aws_iam_user_policy_attachment" "forces_prod_attach_policy" {
  user       = "forces_prod"
  policy_arn = aws_iam_policy.forces_prod_policy.arn
}
