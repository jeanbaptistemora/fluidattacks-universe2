data "aws_iam_policy_document" "bucket_policy" {
  statement {
    sid    = "CloudFront"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.production.iam_arn]
    }
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "${aws_s3_bucket.bucket.arn}/*",
    ]
  }

  statement {
    sid     = "CloudFlare"
    effect  = "Allow"

    actions = [
      "s3:GetObject",
    ]
    resources = [
      "${aws_s3_bucket.bucket.arn}/*",
    ]

    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.bucket.id
  policy = data.aws_iam_policy_document.bucket_policy.json
}
