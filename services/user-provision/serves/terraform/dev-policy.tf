data "aws_iam_policy_document" "serves-dev-policy-data" {

  # S3 serves prod bucket
  statement {
    effect  = "Allow"
    actions = [
      "s3:List*",
      "s3:Get*",
      "iam:List*",
      "iam:Get*",
      "route53:List*",
      "route53:Get*",
      "acm:Describe*",
      "acm:List*",
      "lambda:Get*",
      "lambda:List*",
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
    ]
    resources = [
      "*"
    ]
  }
}
resource "aws_iam_policy" "serves-dev-policy" {
  description = "serves-dev policy"
  name        = "serves-dev-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.serves-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "serves-dev-attach-policy" {
  user       = "serves-dev"
  policy_arn = aws_iam_policy.serves-dev-policy.arn
}
