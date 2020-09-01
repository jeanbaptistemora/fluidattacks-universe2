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

resource "aws_iam_user" "melts-dev" {
  name = var.user-name
  path = "/user-provision/"
}

resource "aws_iam_access_key" "melts-dev-key-1" {
  user = var.user-name
}

resource "aws_iam_access_key" "melts-dev-key-2" {
  user = var.user-name
}
