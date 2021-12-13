data "aws_iam_policy_document" "integrates-prod-key" {

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
        module.external.aws_iam_roles["makes_prod"].arn,
        module.external.aws_iam_roles["prod_integrates"].arn,
        module.external.aws_iam_users["prod_integrates"].arn,
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
        module.external.aws_iam_roles["makes_prod"].arn,
        module.external.aws_iam_roles["prod_integrates"].arn,
        module.external.aws_iam_users["prod_integrates"].arn,
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
        module.external.aws_iam_roles["makes_prod"].arn,
        module.external.aws_iam_roles["prod_integrates"].arn,
        module.external.aws_iam_users["prod_integrates"].arn,
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

resource "aws_kms_key" "integrates-prod-key" {
  description             = "production kms key for integrates prod."
  policy                  = data.aws_iam_policy_document.integrates-prod-key.json
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = {
    "Name"            = "integrates-prod"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_kms_alias" "integrates-prod-key" {
  name          = "alias/integrates-prod-kms"
  target_key_id = aws_kms_key.integrates-prod-key.key_id
}
