data "aws_iam_policy_document" "key_sorts" {
  statement {
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_sorts",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_sorts",
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_sorts",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_sorts",
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_sorts",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_sorts",
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

resource "aws_kms_key" "key_sorts" {
  policy                  = data.aws_iam_policy_document.key_sorts.json
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = {
    "Name"               = "sorts-kms"
    "management:area"    = "cost"
    "management:product" = "sorts"
    "management:type"    = "product"
  }
}

resource "aws_kms_alias" "key_sorts" {
  name          = "alias/sorts_prod"
  target_key_id = aws_kms_key.key_sorts.key_id
}
