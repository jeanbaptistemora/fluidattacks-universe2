data "aws_iam_policy_document" "asserts-dev-policy-data" {

  # S3 state files
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-*",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/asserts-secret-management.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-*/user-provision-asserts-*.tfstate",
    ]
  }

  # KMS read keys
  statement {
    effect = "Allow"
    actions = [
      "kms:List*",
      "kms:Get*",
      "kms:Describe*"
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
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/asserts-dev-*"
    ]
  }
}
resource "aws_iam_policy" "asserts-dev-policy" {
  description = "asserts-dev policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.asserts-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "asserts-dev-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.asserts-dev-policy.arn
}
