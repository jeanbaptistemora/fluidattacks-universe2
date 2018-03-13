data "aws_iam_policy_document" "ssofinance-policy" {
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithSAML"
    ]
    principals {
      type = "Federated"
      identifiers = [
        "${var.ssofinance}"
      ]
    }
    condition {
      test     = "StringEquals"
      variable = "SAML:aud"

      values = [
        "https://signin.aws.amazon.com/saml"
      ]
    }
  }
}

resource "aws_iam_role" "SSO_Finance" {
  name = "SSO_Finance"

  assume_role_policy = "${data.aws_iam_policy_document.ssofinance-policy.json}"
}
