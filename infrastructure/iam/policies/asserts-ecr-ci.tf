data "aws_iam_policy_document" "asserts-ecr-ci-data" {

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

resource "aws_iam_policy" "asserts-ecr-ci-policy" {
  name        = "asserts-ecr-ci-policy"
  path        = "/asserts/"
  description = "Policy for asserts ECR container image deployment"

  policy = "${data.aws_iam_policy_document.asserts-ecr-ci-data.json}"
}
