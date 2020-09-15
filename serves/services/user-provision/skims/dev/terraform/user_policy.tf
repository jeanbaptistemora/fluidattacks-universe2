data "aws_iam_policy_document" "skims_dev_policy_data" {
  # IAM and AWS SSO role
  statement {
    effect = "Allow"
    actions = [
      "iam:GetUser",
      "iam:GetRole",
      "iam:GetPolicy",
      "iam:GetPolicyVersion",
      "iam:ListAccessKeys",
      "iam:ListAttachedUserPolicies",
      "iam:ListAttachedRolePolicies",
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user_provision/skims-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/skims-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/skims-*",
    ]
  }
}

resource "aws_iam_policy" "skims_dev_policy" {
  description = "skims_dev policy"
  name        = "${var.user_name}_policy"
  path        = "/user_provision/"
  policy      = data.aws_iam_policy_document.skims_dev_policy_data.json
}

resource "aws_iam_user_policy_attachment" "skims_dev_attach_policy" {
  user       = var.user_name
  policy_arn = aws_iam_policy.skims_dev_policy.arn
}
