data "aws_iam_policy_document" "sso-policy" {
  statement {
    sid = ""
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithSAML"
    ]
    principals {
      type = "Federated"
      identifiers = [
        "arn:aws:iam::205810638802:saml-provider/OneLogin"
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

resource "aws_iam_role" "SSO" {
  name = "SSO"

  assume_role_policy = "${data.aws_iam_policy_document.sso-policy.json}"
}
