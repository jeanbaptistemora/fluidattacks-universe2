data "aws_iam_policy_document" "integrates-prod-s3-policy-data" {
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::fluidintegrates*/*",
      "arn:aws:s3:::fluidintegrates*",
      "arn:aws:s3:::fi.binaryalert*"
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
}

resource "aws_iam_policy" "integrates-prod-s3-policy" {
  description = "integrates-prod policy for S3"
  name        = "${var.user-name}-s3-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-s3-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-s3" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-s3-policy.arn
}
