data "aws_iam_policy_document" "fis3integrator-policy" {
  statement {
    sid = "VisualEditor0"
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "*"
    ]
  }
}

data "aws_iam_policy_document" "fir53review-policy-doc" {
  statement {
    effect = "Allow"
    actions = [
      "route53:GetChange"
    ]
    resources = [
      "arn:aws:route53:::change/*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "route53:ChangeResourceRecordSets"
    ]
    resources = [
      "arn:aws:route53:::hostedzone/${var.mainZoneID}"
    ]
  }
}

resource "aws_iam_policy" "FI_S3INTEGRATION" {
  name        = "FI_S3INTEGRATION"
  path        = "/"
  description = "Policy for FI_S3INTEGRATION"

  policy = "${data.aws_iam_policy_document.fis3integrator-policy.json}"
}

resource "aws_iam_policy" "fir53review-policy" {
  name = "FI_ROUTE53_REVIEW"
  path = "/"
  description = "Policy for Automatic SSL Certificate Generation"
  policy = "${data.aws_iam_policy_document.fir53review-policy-doc.json}"
}