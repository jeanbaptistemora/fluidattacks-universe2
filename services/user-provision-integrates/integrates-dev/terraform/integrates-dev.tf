data "aws_iam_policy_document" "integrates-dev-policy-data" {
  statement {
    effect = "Allow"
    actions = [
      "kms:CreateKey",
      "kms:ListAliases",
      "kms:CreateAlias",
      "kms:UpdateAlias"
    ]
    resources = [
      "*"
    ]
  }

  statement {
    effect  = "Allow"
    actions = ["kms:*"]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/integrates-dev-*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:GetBucketLocation",
      "s3:ListAllMyBuckets"
    ]
    resources = ["*"]
  }

  statement {
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::fluidattacks-terraform-states-dev"]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListObjects"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-dev/*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::servestf/integrates.tfstate",
      "arn:aws:s3:::servestf"
    ]
  }
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::fluidintegrates*/*",
      "arn:aws:s3:::fluidintegrates*",
      "arn:aws:s3:::fi.binaryalert*"
    ]
  }
}

resource "aws_iam_user" "integrates-dev" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "integrates-dev-key" {
  user = aws_iam_user.integrates-dev.name
}

resource "aws_iam_policy" "integrates-dev-policy" {
  description = "Integrates policy for ${var.user-name}"
  name        = "user-provision-policy-${var.user-name}"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-dev-policy.arn
}
