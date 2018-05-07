variable "webBucket" {}

data "aws_iam_policy_document" "blog-policy" {
  statement {
    sid = "VisualEditor0"
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::web.fluid.la/*",
      "arn:aws:s3:::${var.webBucket}/*",
      "arn:aws:s3:::web.fluid.la",
      "arn:aws:s3:::${var.webBucket}"
    ]
  }
}


resource "aws_iam_policy" "Blog_IAM_Policy" {
  name        = "Blog_IAM_Policy"
  path        = "/"
  description = "Policy for web"

  policy = "${data.aws_iam_policy_document.blog-policy.json}"
}
