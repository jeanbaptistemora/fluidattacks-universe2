data "aws_iam_policy_document" "stores-policy" {
  statement {
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::fluidserves/exams/*",
      "arn:aws:s3:::fluidserves",
      "arn:aws:s3:::fluidpersistent",
      "arn:aws:s3:::fluidpersistent/*"
    ]
  }
}

resource "aws_iam_policy" "fluidstores" {
  name        = "fluidstores"
  path        = "/"
  description = "Policy for fluidstores"

  policy = "${data.aws_iam_policy_document.stores-policy.json}"
}
