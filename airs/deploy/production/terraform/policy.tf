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

data "aws_iam_policy_document" "bucket_policy" {
    statement {
    sid    = "Web bucket permissions"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.production.iam_arn]
    }
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "arn:aws:s3:::fluidattacks.com/*",
      "arn:aws:s3:::fluidattacks.com",
    ]
  }
}

resource "aws_s3_bucket_policy" "web-bucket-policy" {
  bucket = aws_s3_bucket.web-bucket.id
  policy = data.aws_iam_policy_document.web-bucket-policy-data.json
}

resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.bucket.id
  policy = data.aws_iam_policy_document.bucket_policy.json
}
