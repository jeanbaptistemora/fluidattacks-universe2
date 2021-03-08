data "aws_iam_policy_document" "sorts_prod_assume_policy" {
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

resource "aws_iam_role" "sorts-prod" {
  name               = "sorts-prod"
  assume_role_policy = data.aws_iam_policy_document.sorts_prod_assume_policy.json

  tags = {
    "Name"               = "sorts-prod"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_role_policy" "sorts-prod_policy" {
  name   = "sorts-prod_policy"
  policy = data.aws_iam_policy_document.sorts_sagemaker_policy.json
  role   = aws_iam_role.sorts_sagemaker.id
}
