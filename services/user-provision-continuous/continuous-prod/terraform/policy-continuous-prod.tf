data "aws_iam_policy_document" "continuous-prod-policy-data" {

  # S3
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/user-provision-continuous-prod.tfstate"
    ]
  }

  # IAM
  statement {
    effect  = "Allow"
    actions = ["iam:*"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/continuous-*",
    ]
  }

  # KMS
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
  statement {
    effect  = "Allow"
    actions = ["kms:*"]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/continuous-prod-*"
    ]
  }

}

resource "aws_iam_policy" "continuous-prod-policy" {
  description = "continuous-prod policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.continuous-prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "continuous-prod-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.continuous-prod-policy.arn
}
