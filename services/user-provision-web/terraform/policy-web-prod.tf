data "aws_iam_policy_document" "integrates-dev-policy-data" {

    # S3
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::web.fluidattacks.com/*"
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
      "arn:aws:s3:::fluidattacks-terraform-states-dev",
      "arn:aws:s3:::fluidattacks-terraform-states-dev/user-provision-web-prod.tfstate"
    ]
  }
}
resource "aws_iam_policy" "web-prod-policy" {
  description = "web-prod policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "web-prod-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.web-prod-policy.arn
}
