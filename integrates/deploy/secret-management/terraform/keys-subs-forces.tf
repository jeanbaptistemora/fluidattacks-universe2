data "aws_iam_policy_document" "key_forces_projects" {
  statement {
    sid    = "Enable IAM User Permissions"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
    actions   = ["kms:*"]
    resources = ["*"]
  }

  statement {
    sid    = "Key Administrators"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/FLUIDServes_TF",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/serves-admin",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/integrates-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/integrates-prod"
      ]
    }
    actions = [
      "kms:Update*",
      "kms:UntagResource",
      "kms:TagResource",
      "kms:ScheduleKeyDeletion",
      "kms:Revoke*",
      "kms:Put*",
      "kms:List*",
      "kms:Get*",
      "kms:Enable*",
      "kms:Disable*",
      "kms:Describe*",
      "kms:Delete*",
      "kms:Create*",
      "kms:CancelKeyDeletion",
    ]
    resources = ["*"]
  }

  statement {
    sid    = "Key Users"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/integrates-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/integrates-prod"
      ]
    }
    actions = [
      "kms:ReEncrypt*",
      "kms:GenerateDataKey*",
      "kms:Encrypt",
      "kms:DescribeKey",
      "kms:Decrypt",
    ]
    resources = ["*"]
  }

  statement {
    sid    = "Attachment Of Persistent Resources"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/integrates-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/integrates-prod"
      ]
    }
    actions = [
      "kms:RevokeGrant",
      "kms:ListGrants",
      "kms:CreateGrant",
    ]
    resources = ["*"]
    condition {
      test     = "Bool"
      variable = "kms:GrantIsForAWSResource"
      values   = ["true"]
    }
  }
}

resource "aws_kms_key" "forces_key" {
  for_each                = { for name in var.projects_forces : name => name }
  description             = "KMS key for forces-${each.value}"
  deletion_window_in_days = 30
  is_enabled              = true

  tags = {
    "Name"               = "Forces key"
    "management:type"    = "production"
    "management:product" = "forces"
  }

  policy = data.aws_iam_policy_document.key_forces_projects.json
}

resource "aws_kms_alias" "keys_aliases" {
  for_each      = { for name in var.projects_forces : name => name }
  name          = "alias/forces_key_${each.value}"
  target_key_id = aws_kms_key.forces_key[each.value].key_id
}
