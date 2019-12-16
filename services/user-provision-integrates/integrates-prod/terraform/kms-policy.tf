data "aws_iam_policy_document" "integrates-prod-kms-policy-data" {
  statement {
    effect = "Allow"
    actions = [
      "kms:UntagResource",
      "kms:TagResource",
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
      "kms:CreateKey"
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["kms:*"]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/fi_binaryalert*",
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/integrates-prod-*"
    ]
  }
}

resource "aws_iam_policy" "integrates-prod-kms-policy" {
  description = "integrates-prod policy for kms"
  name        = "${var.user-name}-kms-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-kms-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-kms" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-kms-policy.arn
}
