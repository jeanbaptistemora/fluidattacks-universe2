data "aws_iam_policy_document" "onelogin-assume-role-policy-data" {
  statement {
    sid = "Onelogin SAML access"
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithSAML"
    ]
    principals {
      type = "Federated"
      identifiers = [aws_iam_saml_provider.onelogin-saml-provider.arn]
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

resource "aws_iam_policy" "onelogin-assume-role-policy" {
  name        = "onelogin-assume-role"
  path        = "/"
  description = "Attach this policy to roles that you want to use with onelogin"

  policy = data.aws_iam_policy_document.onelogin-assume-role-policy-data.json
}
