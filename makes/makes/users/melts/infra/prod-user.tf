data "aws_iam_policy_document" "prod-policy-data" {

  # S3
  statement {
    effect = "Allow"
    actions = [
      "s3:*",
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/melts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/melts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/melts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/melts-*"
    ]
  }

  # IAM
  statement {
    effect = "Allow"
    actions = [
      "iam:*",
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/melts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/melts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/melts-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/melts-*"
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

resource "aws_iam_policy" "prod-policy" {
  description = "melts prod policy"
  name        = "melts-prod-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "prod-attach-policy" {
  user       = "melts-prod"
  policy_arn = aws_iam_policy.prod-policy.arn
}

resource "aws_iam_user" "melts-prod" {
  name = "melts-prod"
  path = "/user-provision/"

  tags = {
    "Name"               = "melts-prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_access_key" "melts-prod-key-1" {
  user = "melts-prod"
}

resource "aws_iam_access_key" "melts-prod-key-2" {
  user = "melts-prod"
}

module "publish_credentials_prod" {
  source       = "../../modules/publish_credentials"
  gitlab_token = var.gitlab_token
  key_1        = aws_iam_access_key.melts-prod-key-1
  key_2        = aws_iam_access_key.melts-prod-key-2
  prefix       = "MELTS_PROD"
  protected    = true
}
