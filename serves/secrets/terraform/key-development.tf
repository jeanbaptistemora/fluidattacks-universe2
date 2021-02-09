data "aws_iam_policy_document" "key-serves-development" {

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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/FLUIDServes_TF",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/serves-admin"
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/FLUIDServes_TF",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/serves-admin"
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/FLUIDServes_TF",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/serves-admin"
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

resource "aws_kms_key" "key-serves-development" {
  description             = "development kms key for serves."
  policy                  = data.aws_iam_policy_document.key-serves-development.json
  deletion_window_in_days = 30
  is_enabled              = true

  tags = {
    "Name"               = "serves-development"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_kms_alias" "key-serves-development" {
  name          = "alias/serves-development"
  target_key_id = aws_kms_key.key-serves-development.key_id
}
