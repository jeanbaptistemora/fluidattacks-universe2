data "aws_iam_policy_document" "serves-admin-policy-data" {

  statement {
    sid = "GeneralAdmin"
    effect = "Allow"
    actions = [
      "sns:*",
      "rds:*",
      "s3:*",
      "dynamodb:Scan",
      "elasticloadbalancing:*",
      "autoscaling:*",
      "iam:*",
      "secretsmanager:*",
      "cloudwatch:*",
      "kms:*",
      "route53:*",
      "ecr:*",
      "ec2:*",
      "eks:*",
      "elasticache:*"
    ]
    resources = [
      "*"
    ]
  }
}

data "aws_iam_policy_document" "onelogin-assume-role-policy-data" {
  statement {
    sid = "OneloginSAMLAccess"
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithSAML"
    ]
    principals {
      type = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:saml-provider/onelogin-saml-provider"]
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

resource "aws_iam_policy" "serves-admin-policy" {
  name        = "serves-admin"
  path        = "/serves/"
  description = "Policy for serves administration"

  policy = data.aws_iam_policy_document.serves-admin-policy-data.json
}

resource "aws_iam_role" "serves-admin-role" {
  name = "serves-admin"

  assume_role_policy = data.aws_iam_policy_document.onelogin-assume-role-policy-data.json
}

resource "aws_iam_role_policy_attachment" "test-attach" {
  role       = aws_iam_role.serves-admin-role.name
  policy_arn = aws_iam_policy.serves-admin-policy.arn
}
