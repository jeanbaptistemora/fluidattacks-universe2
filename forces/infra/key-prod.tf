data "aws_iam_policy_document" "key-forces-production" {

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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user_provision/forces_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:*/prod_forces",
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
    sid    = "key Managger"
    effect = "Allow"
    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user_provision/forces_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:*/prod_forces",
      ]
    }
    actions = [
      "kms:DescribeKey",
      "kms:GetKeyPolicy",
      "kms:GetKeyRotationStatus",
      "kms:ListResourceTags",
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user_provision/forces_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:*/prod_forces",
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user_provision/forces_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:*/prod_forces",
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

resource "aws_kms_key" "key-forces-prod" {
  description             = "production kms key for forces."
  policy                  = data.aws_iam_policy_document.key-forces-production.json
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = {
    "Name"            = "forces-production"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_kms_alias" "key-forces-prod" {
  name          = "alias/forces-prod"
  target_key_id = aws_kms_key.key-forces-prod.key_id
}
