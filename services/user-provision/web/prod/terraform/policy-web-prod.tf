data "aws_iam_policy_document" "web-prod-policy-data" {

  # S3 web bucket
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::web.fluidattacks.com/*",
      "arn:aws:s3:::web.fluidattacks.com",
      "arn:aws:s3:::web.eph.fluidattacks.com/*",
      "arn:aws:s3:::web.eph.fluidattacks.com",
    ]
  }

  # S3 state files
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-*",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/web-secret-management.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-*/user-provision-web-*.tfstate",
    ]
  }

  # IAM full permissions over owned users, roles and policies
  statement {
    effect  = "Allow"
    actions = [
      "iam:*"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/web-*",
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
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/web-*"
    ]
  }
}

resource "aws_iam_policy" "web-prod-policy" {
  description = "web-prod policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.web-prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "web-prod-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.web-prod-policy.arn
}
