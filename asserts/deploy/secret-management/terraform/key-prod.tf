data "aws_iam_policy_document" "asserts-prod-key" {

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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/asserts-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/asserts-prod"
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/asserts-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/asserts-prod"
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/asserts-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/asserts-prod"
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

resource "aws_kms_key" "asserts-prod-key" {
  description             = "production kms key for asserts prod."
  policy                  = data.aws_iam_policy_document.asserts-prod-key.json
  deletion_window_in_days = 30
  is_enabled              = true
}

resource "aws_kms_alias" "asserts-prod-key" {
  name          = "alias/asserts-prod"
  target_key_id = aws_kms_key.asserts-prod-key.key_id
}
