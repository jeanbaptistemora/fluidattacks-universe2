data "aws_iam_policy_document" "kms-admin" {

  statement {
    sid = "kms-all-permissions"
    effect = "Allow"
    actions = [
      "kms:DescribeCustomKeyStores",
      "kms:ListKeys",
      "kms:DeleteCustomKeyStore",
      "kms:GenerateRandom",
      "kms:UpdateCustomKeyStore",
      "kms:ListAliases",
      "kms:DisconnectCustomKeyStore",
      "kms:CreateKey",
      "kms:ConnectCustomKeyStore",
      "kms:CreateCustomKeyStore"
    ]
    resources = [
      "*"
    ]
  }

  statement {
    sid = "kms-alises-and-keys"
    effect = "Allow"
    actions = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:*:*:alias/*",
      "arn:aws:kms:*:*:key/*"
    ]
  }
}

resource "aws_iam_policy" "kms-admin" {
  name        = "kms-admin"
  path        = "/"
  description = "Full permissions over KMS"

  policy = "${data.aws_iam_policy_document.kms-admin.json}"
}
