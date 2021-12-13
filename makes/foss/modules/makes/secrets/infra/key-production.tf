data "aws_iam_policy_document" "key-serves-production" {

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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_makes"
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_makes"
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/serves-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/prod_makes",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/prod_makes"
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

resource "aws_kms_key" "key-serves-production" {
  description             = "production kms key for serves."
  policy                  = data.aws_iam_policy_document.key-serves-production.json
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = {
    "Name"            = "serves-production"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_kms_alias" "key-serves-production" {
  name          = "alias/serves-production"
  target_key_id = aws_kms_key.key-serves-production.key_id
}
