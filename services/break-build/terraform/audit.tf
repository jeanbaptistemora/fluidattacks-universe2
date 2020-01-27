data "aws_iam_policy_document" "break-build-audit-data" {

  statement {
    sid    = "iamBreakBuildAudit"
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "break-build-audit-policy" {
  name        = "break-build-audit-policy"
  path        = "/asserts/"
  description = "Policy to assume roles of external entities"

  policy = data.aws_iam_policy_document.break-build-audit-data.json
}

resource "aws_iam_user" "break-build-audit-user" {
  name = "break-build-audit"
  path = "/asserts/"
}

resource "aws_iam_user_policy_attachment" "attach-break-build-audit-policy" {
  policy_arn = aws_iam_policy.break-build-audit-policy.arn
  user       = aws_iam_user.break-build-audit-user.name
}
