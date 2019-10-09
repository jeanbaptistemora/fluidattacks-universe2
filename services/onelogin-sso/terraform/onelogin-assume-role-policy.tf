data "aws_iam_policy_document" "onelogin-assume-role-policy-data" {
  statement {
    sid = "OneloginSAMLAccess"
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
