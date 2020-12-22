data "aws_iam_policy_document" "web-ephemeral-bucket-policy-data" {
  statement {
    sid    = "CloudFront"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.web-ephemeral-oai.iam_arn]
    }
    actions = [
      "s3:GetObject",
    ]
    resources = [
      "${aws_s3_bucket.web-ephemeral-bucket.arn}/*",
    ]
  }

  statement {
    sid     = "CloudFlare"
    effect  = "Allow"

    actions = [
      "s3:GetObject",
    ]
    resources = [
      "${aws_s3_bucket.web-ephemeral-bucket.arn}/*",
    ]

    condition {
      test     = "IpAddress"
      variable = "aws:SourceIp"
      values   = data.cloudflare_ip_ranges.cloudflare.cidr_blocks
    }
  }
}

resource "aws_s3_bucket_policy" "web-bucket-policy" {
  bucket = aws_s3_bucket.web-ephemeral-bucket.id
  policy = data.aws_iam_policy_document.web-ephemeral-bucket-policy-data.json
}
