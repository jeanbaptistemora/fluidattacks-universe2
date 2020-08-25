data "aws_iam_policy_document" "prod-policy-data" {

  # DynamoDB
  statement {
    effect  = "Allow"
    actions = [
      "dynamodb:*",
    ]
    resources = ["*"]
  }

  # Redshift
  statement {
    effect  = "Allow"
    actions = [
      "redshift:*",
    ]
    resources = [
      "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:cluster:fluid-redshift"
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
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/observes-*"
    ]
  }
}

resource "aws_iam_policy" "prod-policy" {
  description = "observes prod policy"
  name        = "observes-prod-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "prod-attach-policy" {
  user       = "observes-prod"
  policy_arn = aws_iam_policy.prod-policy.arn
}

resource "aws_iam_user" "prod" {
  name = "observes-prod"
  path = "/user-provision/"
}

resource "aws_iam_access_key" "prod-key-1" {
  user = "observes-prod"
}

resource "aws_iam_access_key" "prod-key-2" {
  user = "observes-prod"
}
