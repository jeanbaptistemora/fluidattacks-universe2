data "aws_iam_policy_document" "asserts-admin-policy-data" {

  statement {
    sid = "ecrPushToAssertsRegistries"
    effect = "Allow"
    actions = [
      "ecr:PutImage"
    ]
    resources = [
      "arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/asserts-*"
    ]
  }

  statement {
    sid = "authToken"
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken"
    ]
    resources = [
      "*"
    ]
  }

}

resource "aws_iam_policy" "asserts-admin-policy" {
  name        = "asserts-admin-policy"
  path        = "/asserts/"
  description = "Policy for asserts admin"

  policy = "${data.aws_iam_policy_document.asserts-admin-policy-data.json}"
}
