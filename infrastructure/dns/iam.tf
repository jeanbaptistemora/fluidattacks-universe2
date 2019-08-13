data "aws_iam_policy_document" "fir53review-policy-doc" {
  statement {
    effect = "Allow"
    actions = [
      "route53:GetChange",
    ]
    resources = [
      "arn:aws:route53:::change/*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "route53:ChangeResourceRecordSets",
    ]
    resources = [
      "arn:aws:route53:::hostedzone/${aws_route53_zone.fs_maindomain.zone_id}",
    ]
  }
}

resource "aws_iam_policy" "fir53review-policy" {
  name        = "FluidIntegrates_DNSReview"
  path        = "/"
  description = "Policy for Automatic SSL Certificate Generation"
  policy      = data.aws_iam_policy_document.fir53review-policy-doc.json
}

