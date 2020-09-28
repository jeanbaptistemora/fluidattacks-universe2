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
      "arn:aws:s3:::fluidattacks-terraform-states-prod/*"
    ]
  }

  # IAM
  statement {
    effect = "Allow"
    actions = [
      "iam:List*",
      "iam:Get*"
    ]
    resources = ["*"]
  }

  # DynamoDB
  statement {
    effect  = "Allow"
    actions = [
      "dynamodb:Describe*",
      "dynamodb:List*",
    ]
    resources = [
      "*"
    ]
  }

  # Redshift
  statement {
    effect  = "Allow"
    actions = [
      "redshift:Describe*",
      "redshift:List*",
      "redshift:View*",
      "redshift:Fetch*",
      "redshift:View*",
    ]
    resources = [
      "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:cluster:fluid-redshift"
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
  description = "observes dev policy"
  name        = "observes-dev-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "dev-attach-policy" {
  user       = "observes-dev"
  policy_arn = aws_iam_policy.dev-policy.arn
}

resource "aws_iam_user" "dev" {
  name = "observes-dev"
  path = "/user-provision/"

  tags = {
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_access_key" "dev-key-1" {
  user = "observes-dev"
}

resource "aws_iam_access_key" "dev-key-2" {
  user = "observes-dev"
}
