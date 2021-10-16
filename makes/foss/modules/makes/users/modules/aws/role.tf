resource "aws_iam_role" "main" {
  name                 = var.name
  assume_role_policy   = data.aws_iam_policy_document.okta_assume_role_policy.json
  max_session_duration = "32400"

  tags = {
    "Name"               = var.name
    "management:type"    = var.type
    "management:product" = var.product
  }
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = var.policy
}

data "aws_caller_identity" "current" {}
data "aws_iam_policy_document" "okta_assume_role_policy" {
  statement {
    sid    = "OktaSAMLAccess"
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithSAML"
    ]
    principals {
      type        = "Federated"
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
