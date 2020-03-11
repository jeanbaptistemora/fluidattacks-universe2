data "aws_iam_policy_document" "web-ephemeral-bucket-policy-data" {
    statement {
    sid    = "Web bucket permissions"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.web-ephemeral-oai.iam_arn]
    }
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::web.eph.fluidattacks.com/*",
      "arn:aws:s3:::web.eph.fluidattacks.com",
    ]
  }
}

resource "aws_s3_bucket_policy" "web-bucket-policy" {
  bucket = aws_s3_bucket.web-ephemeral-bucket.id
  policy = data.aws_iam_policy_document.web-ephemeral-bucket-policy-data.json
}
