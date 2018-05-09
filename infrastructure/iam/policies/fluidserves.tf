data "aws_iam_policy_document" "serves-policy" {
  statement {
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "fluidserves" {
  name        = "fluidserves"
  path        = "/"
  description = "Policy for fluidserves"

  policy = "${data.aws_iam_policy_document.serves-policy.json}"
}
