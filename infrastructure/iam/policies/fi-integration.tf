data "aws_iam_policy_document" "fis3integrator-policy" {
  statement {
    sid = "VisualEditor0"
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "*"
    ]
  }
}


resource "aws_iam_policy" "FI_S3INTEGRATION" {
  name        = "FI_S3INTEGRATION"
  path        = "/"
  description = "Policy for FI_S3INTEGRATION"

  policy = "${data.aws_iam_policy_document.fis3integrator-policy.json}"
}
