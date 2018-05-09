resource "aws_iam_user" "fir53review" {
  name = "FI_ROUTE53_REVIEW"
  path = "/"
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
      "arn:aws:route53:::hostedzone/${aws_route53_zone.fs_maindomain.zone_id}"
    ]
  }
}

resource "aws_iam_policy" "fir53review-policy" {
  name = "FI_ROUTE53_REVIEW"
  path = "/"
  description = "Policy for Automatic SSL Certificate Generation"
  policy = "${data.aws_iam_policy_document.fir53review-policy-doc.json}"
}

resource "aws_iam_user_policy_attachment" "fir53review-attach" {
  user       = "${aws_iam_user.fir53review.name}"
  policy_arn = "${aws_iam_policy.fir53review-policy.arn}"
}
