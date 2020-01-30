data "aws_iam_policy_document" "continuous-dev-policy-data" {

  # S3 read prod continuous-secret-management tfstate
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/continuous-secret-management.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/break-build.tfstate"
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

  # KMS FUll permissions over owned KMS keys
  statement {
    effect  = "Allow"
    actions = ["kms:*"]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/continuous-dev-*"
    ]
  }
}

resource "aws_iam_policy" "continuous-dev-policy" {
  description = "continuous-dev policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.continuous-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "continuous-dev-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.continuous-dev-policy.arn
}
