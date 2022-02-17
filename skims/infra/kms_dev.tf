data "aws_iam_policy_document" "key_skims_dev" {

  statement {
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_skims",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_skims",
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_skims",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_skims",
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_skims",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_skims",
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
    "management:area"    = "innovation"
    "management:product" = "skims"
    "management:type"    = "product"
  }
}

resource "aws_kms_alias" "key_skims_dev" {
  name          = "alias/skims_dev"
  target_key_id = aws_kms_key.key_skims_dev.key_id
}
