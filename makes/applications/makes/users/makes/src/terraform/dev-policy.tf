data "aws_iam_policy_document" "dev-policy-data" {

  statement {
    effect = "Allow"
    actions = [
      "batch:Describe*",
      "batch:Get*",
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
      "dynamodb:Describe*",
      "dynamodb:List*",
      "events:Describe*",
      "events:List*",
      "elasticloadbalancing:Describe*",
      "cloudwatch:List*",
      "cloudwatch:Describe*",
      "ec2:Describe*",
      "ec2:Get*",
      "eks:Describe*",
      "eks:List*",
      "autoscaling:Describe*",
      "autoscaling:Get*",
    ]
    resources = [
      "*"
    ]
  }

  # S3 doc development bucket
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:Get*",
      "s3:PutObject",
      "s3:PutObjectAcl",
      "s3:DeleteObject*",
    ]
    resources = [
      "arn:aws:s3:::doc-dev.fluidattacks.com/*",
      "arn:aws:s3:::doc-dev.fluidattacks.com",
    ]
  }

  # S3 doc upload multimedia
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:Get*",
      "s3:PutObject",
      "s3:PutObjectAcl",
    ]
    resources = [
      "arn:aws:s3:::doc.fluidattacks.com/multimedia/*",
      "arn:aws:s3:::doc.fluidattacks.com",
    ]
  }

}

resource "aws_iam_policy" "dev-policy" {
  description = "serves dev policy"
  name        = "serves-dev-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "dev-attach-policy" {
  user       = "serves-dev"
  policy_arn = aws_iam_policy.dev-policy.arn
}
