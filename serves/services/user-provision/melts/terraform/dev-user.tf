data "aws_iam_policy_document" "dev-policy-data" {

  # S3
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/melts-*"
    ]
  }

  # IAM
  statement {
    effect = "Allow"
    actions = [
      "iam:List*",
      "iam:Get*"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/melts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/melts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/melts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/melts-*",
    ]
  }

  # KMS
  statement {
    effect = "Allow"
    actions = [
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "dev-policy" {
  description = "melts dev policy"
  name        = "melts-dev-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "dev-attach-policy" {
  user       = "melts-dev"
  policy_arn = aws_iam_policy.dev-policy.arn
}

resource "aws_iam_user" "melts-dev" {
  name = "melts-dev" 
  path = "/user-provision/"
}

resource "aws_iam_access_key" "melts-dev-key-1" {
  user = "melts-dev" 
}

resource "aws_iam_access_key" "melts-dev-key-2" {
  user = "melts-dev" 
}
