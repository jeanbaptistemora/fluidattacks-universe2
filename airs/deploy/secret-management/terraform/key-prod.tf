data "aws_iam_policy_document" "key-web-production" {

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
      type        = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/FLUIDServes_TF",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/serves-admin",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/web-admin",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-prod"
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
      type        = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/FLUIDServes_TF",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/serves-admin",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/web-admin",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-prod"
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
      type        = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/FLUIDServes_TF",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/serves-admin",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/web-admin",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-prod"
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
      values   = [
        "true",
      ]
    }
  }
}

resource "aws_kms_key" "key-web-prod" {
  description             = "production kms key for web."
  policy                  = data.aws_iam_policy_document.key-web-production.json
  deletion_window_in_days = 30
  is_enabled              = true

  tags = {
    "management:type"    = "production"
    "management:product" = "airs"
  }
}

resource "aws_kms_alias" "key-web-prod" {
  name          = "alias/web-prod"
  target_key_id = aws_kms_key.key-web-prod.key_id
}
