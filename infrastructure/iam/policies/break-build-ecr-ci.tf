data "aws_iam_policy_document" "break-build-ecr-ci-data" {

  statement {
    sid = "ecrPushToAssertsRegistries"
    effect = "Allow"
    actions = [
      "ecr:PutImage",
      "ecr:BatchCheckLayerAvailability",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload"
    ]
    resources = [
      "arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/break-build-*"
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

resource "aws_iam_policy" "break-build-ecr-ci-policy" {
  name        = "break-build-ecr-ci-policy"
  path        = "/asserts/"
  description = "Policy for break build ECR container image deployment"

  policy = "${data.aws_iam_policy_document.break-build-ecr-ci-data.json}"
}
