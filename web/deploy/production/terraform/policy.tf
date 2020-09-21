data "aws_iam_policy_document" "web-bucket-policy-data" {
    statement {
    sid    = "Web bucket permissions"
    effect = "Allow"
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "arn:aws:s3:::web.fluidattacks.com/*",
      "arn:aws:s3:::web.fluidattacks.com",
    ]
  }
}

resource "aws_s3_bucket_policy" "web-bucket-policy" {
  bucket = aws_s3_bucket.web-bucket.id
  policy = data.aws_iam_policy_document.web-bucket-policy-data.json
}
