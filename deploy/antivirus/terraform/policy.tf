

data "aws_iam_policy_document" "s3_antivirus_access" {
  statement {
    sid       = "AllowPublic"
    effect    = "Allow"
    actions   = [
      "s3:GetObject",
      "s3:GetObjectTagging",
    ]
    resources = [
      "${aws_s3_bucket.fi_antivirus_bucket.arn}/*"
    ]

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}

resource "aws_s3_bucket_policy" "fi_antivirus_bucket_policy" {
  bucket = aws_s3_bucket.fi_antivirus_bucket.id
  policy = data.aws_iam_policy_document.s3_antivirus_access.json
}
