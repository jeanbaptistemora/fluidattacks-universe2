# Production

data "aws_iam_policy_document" "key_prod" {

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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/airs_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-prod",
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/airs_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-prod",
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/airs_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-prod",
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

resource "aws_kms_key" "prod" {
  description             = "production kms key for web."
  policy                  = data.aws_iam_policy_document.key_prod.json
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = {
    "Name"               = "web-production"
    "management:type"    = "production"
    "management:product" = "airs"
  }
}

resource "aws_kms_alias" "prod" {
  name          = "alias/web-prod"
  target_key_id = aws_kms_key.prod.key_id
}


# Development

data "aws_iam_policy_document" "key_dev" {

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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/airs_dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/airs_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/development",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-prod",
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/airs_dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/airs_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/development",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-dev",
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
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/makes_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/airs_dev",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/airs_prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/development",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-prod",
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/user-provision/web-dev"
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

resource "aws_kms_key" "dev" {
  description             = "Normal user kms key for web."
  policy                  = data.aws_iam_policy_document.key_dev.json
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = {
    "Name"               = "web-development"
    "management:type"    = "development"
    "management:product" = "airs"
  }
}

resource "aws_kms_alias" "dev" {
  name          = "alias/web-dev"
  target_key_id = aws_kms_key.dev.key_id
}
