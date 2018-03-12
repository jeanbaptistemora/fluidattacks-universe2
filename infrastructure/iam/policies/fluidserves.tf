data "aws_iam_policy_document" "serves-policy" {
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

resource "aws_iam_policy" "fluidserves" {
  name        = "fluidserves"
  path        = "/"
  description = "Policy for fluidserves"

  policy = "${data.aws_iam_policy_document.serves-policy.json}"
}
