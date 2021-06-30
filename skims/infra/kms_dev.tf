data "aws_iam_policy_document" "key_skims_dev" {

  statement {
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/FLUIDServes_TF",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user_provision/skims_prod",
      ]
    }
    actions = [
      "kms:*",
    ]
    resources = [
      "*"
    ]
  }

  statement {
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user_provision/skims_dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user_provision/skims_prod",
      ]
    }
    actions = [
      "kms:Encrypt",
      "kms:Decrypt",
      "kms:ReEncrypt*",
      "kms:GenerateDataKey*",
      "kms:DescribeKey",
    ]
    resources = [
      "*"
    ]
  }

  statement {
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user_provision/skims_dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user_provision/skims_prod",
      ]
    }
    actions = [
      "kms:CreateGrant",
      "kms:ListGrants",
      "kms:RevokeGrant",
    ]
    resources = [
      "*"
    ]
    condition {
      test     = "Bool"
      variable = "kms:GrantIsForAWSResource"
      values = [
        "true",
      ]
    }
  }
}

resource "aws_kms_key" "key_skims_dev" {
  policy                  = data.aws_iam_policy_document.key_skims_dev.json
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = {
    "Name"               = "skims-development"
    "management:type"    = "development"
    "management:product" = "skims"
  }
}

resource "aws_kms_alias" "key_skims_dev" {
  name          = "alias/skims_dev"
  target_key_id = aws_kms_key.key_skims_dev.key_id
}
