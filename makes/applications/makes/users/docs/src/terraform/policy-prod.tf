data "aws_iam_policy_document" "prod" {

  # S3 prod and ephemeral buckets
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::docs.fluidattacks.com/*",
      "arn:aws:s3:::docs.fluidattacks.com",
      "arn:aws:s3:::docs-dev.fluidattacks.com/*",
      "arn:aws:s3:::docs-dev.fluidattacks.com",
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
      "arn:aws:s3:::fluidattacks-terraform-states-prod/docs*",
    ]
  }

  # IAM full permissions over owned users, roles and policies
  statement {
    effect = "Allow"
    actions = [
      "iam:*"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/docs*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/docs*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/docs*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/docs*",
    ]
  }

  # ACM create, read and delete certificate
  statement {
    effect = "Allow"
    actions = [
      "acm:RequestCertificate",
      "acm:DescribeCertificate",
      "acm:ListTagsForCertificate",
      "acm:AddTagsToCertificate",
      "acm:DeleteCertificate",
    ]
    resources = [
      "*",
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

resource "aws_iam_policy" "prod" {
  name   = "docs_prod"
  path   = "/user-provision/"
  policy = data.aws_iam_policy_document.prod.json
}

resource "aws_iam_user_policy_attachment" "prod" {
  user       = "docs_prod"
  policy_arn = aws_iam_policy.prod.arn
}
