data "aws_iam_policy_document" "integrates-dev-policy-data" {
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
      "*"
    ]
  }

}

resource "aws_iam_user" "integrates-dev" {
  name = "integrates-dev"
  path = "/user-provision/"
}

resource "aws_iam_access_key" "integrates-dev-key" {
  user = aws_iam_user.integrates-dev.name
}

resource "aws_iam_policy" "integrates-dev-policy" {
  description = "Integrates policy for ${aws_iam_user.integrates-dev.name}"
  name        = "user-provision-policy-${aws_iam_user.integrates-dev.name}"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy" {
  user       = aws_iam_user.integrates-dev.name
  policy_arn = aws_iam_policy.integrates-dev-policy.arn
}
