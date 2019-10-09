data "aws_iam_policy_document" "onelogin-saml-policy-data" {
  statement {
    sid     = "AllowAssumeRoleForAnotherAccount"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "AWS"
      identifiers = [var.onelogin-account-id]
    }

    condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"

      values = [var.onelogin-external-id]
    }
  }
}

resource "aws_iam_role" "onelogin-saml-role" {
  name               = "onelogin-access-role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.onelogin-saml-policy-data.json
}
