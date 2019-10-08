data "aws_iam_policy_document" "onelogin-saml-policy" {
  statement {
    sid = "Onelogin SAML access"
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithSAML"
    ]
    principals {
      type = "Federated"
      identifiers = [
        aws_iam_saml_provider.onelogin-saml-provider.arn
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

resource "aws_iam_role" "onelogin-saml-role" {
  name = "SSO"

  assume_role_policy = data.aws_iam_policy_document.onelogin-saml-policy.json
}
