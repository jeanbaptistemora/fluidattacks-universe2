data "aws_iam_policy_document" "okta" {

  statement {
    sid    = "Enable IAM User Permissions"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
    actions = [
      "kms:*"
    ]
    resources = [
      "*"
    ]
  }

  statement {
    sid    = "Key Administrators"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-prod",
      ]
    }
    actions = [
      "kms:Create*",
      "kms:Describe*",
      "kms:Enable*",
      "kms:List*",
      "kms:Put*",
      "kms:Update*",
      "kms:Revoke*",
      "kms:Disable*",
      "kms:Get*",
      "kms:Delete*",
      "kms:TagResource",
      "kms:UntagResource",
      "kms:ScheduleKeyDeletion",
      "kms:CancelKeyDeletion",
    ]
    resources = [
      "*"
    ]
  }

  statement {
    sid    = "Key Users"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-prod",
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
    sid    = "Attachment Of Persistent Resources"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-prod",
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

resource "aws_kms_key" "okta" {
  policy                  = data.aws_iam_policy_document.okta.json
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = {
    "Name"            = "makes-okta"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_kms_alias" "okta" {
  name          = "alias/makes-okta"
  target_key_id = aws_kms_key.okta.key_id
}
