data "aws_iam_policy_document" "onelogin-saml-assume-policy-data" {
  statement {
    sid     = "AllowAssumeRoleForOneloginAccount"
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

data "aws_iam_policy_document" "onelogin-saml-policy-data" {
  statement {
    sid = "AllowListAliasesAndRoles"
    effect = "Allow"
    actions = [
      "iam:ListAccountAliases",
      "iam:ListRoles",
    ]
    resources = [
      "*",
    ]
  }
}

resource "aws_iam_role" "onelogin-saml-role" {
  name               = "onelogin-access-role"
  path               = "/"
  assume_role_policy = data.aws_iam_policy_document.onelogin-saml-assume-policy-data.json
}

resource "aws_iam_policy" "onelogin-saml-policy" {
  name        = "onelogin-access-role"
  path        = "/"
  description = "Policy for allowing onelogin to list account aliases and roles"
  policy = data.aws_iam_policy_document.onelogin-saml-policy-data.json
}

resource "aws_iam_role_policy_attachment" "onelogin-saml-role-attach-policy" {
  role       = aws_iam_role.onelogin-saml-role.name
  policy_arn = aws_iam_policy.onelogin-saml-policy.arn
}
