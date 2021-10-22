data "aws_iam_policy_document" "integrates-dev-key" {

  statement {
    sid    = "Enable IAM User Permissions"
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = [module.external.aws_root.arn]
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
        module.external.aws_iam_roles["dev"].arn,
        module.external.aws_iam_roles["integrates-dev"].arn,
        module.external.aws_iam_roles["makes_prod"].arn,
        module.external.aws_iam_users["dev"].arn,
        module.external.aws_iam_users["integrates-dev"].arn,
        module.external.aws_iam_users["integrates-prod"].arn,
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
        module.external.aws_iam_roles["dev"].arn,
        module.external.aws_iam_roles["integrates-dev"].arn,
        module.external.aws_iam_roles["makes_prod"].arn,
        module.external.aws_iam_users["dev"].arn,
        module.external.aws_iam_users["integrates-dev"].arn,
        module.external.aws_iam_users["integrates-prod"].arn,
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
        module.external.aws_iam_roles["dev"].arn,
        module.external.aws_iam_roles["integrates-dev"].arn,
        module.external.aws_iam_roles["makes_prod"].arn,
        module.external.aws_iam_users["dev"].arn,
        module.external.aws_iam_users["integrates-dev"].arn,
        module.external.aws_iam_users["integrates-prod"].arn,
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

resource "aws_kms_key" "integrates-dev-key" {
  description             = "kms key for integrates dev."
  policy                  = data.aws_iam_policy_document.integrates-dev-key.json
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = {
    "Name"               = "integrates-dev"
    "management:type"    = "development"
    "management:product" = "integrates"
  }
}

resource "aws_kms_alias" "integrates-dev-key" {
  name          = "alias/integrates-dev-kms"
  target_key_id = aws_kms_key.integrates-dev-key.key_id
}
