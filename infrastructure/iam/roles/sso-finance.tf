data "aws_iam_policy_document" "okta-assume-role-policy-data" {
  statement {
    sid = "OktaSAMLAccess"
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithSAML"
    ]
    principals {
      type = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:saml-provider/okta-saml-provider"]
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
  name               = "SSO_Finance"
  assume_role_policy = "${data.aws_iam_policy_document.okta-assume-role-policy-data.json}"
}
