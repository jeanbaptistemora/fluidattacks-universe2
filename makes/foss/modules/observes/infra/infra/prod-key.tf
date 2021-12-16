data "aws_iam_policy_document" "key-prod" {

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
        module.external.aws_iam_roles["prod_makes"].arn,
        module.external.aws_iam_roles["prod_observes"].arn,
        module.external.aws_iam_users["prod_makes"].arn,
        module.external.aws_iam_users["prod_observes"].arn,
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
        module.external.aws_iam_roles["prod_makes"].arn,
        module.external.aws_iam_roles["prod_observes"].arn,
        module.external.aws_iam_users["prod_makes"].arn,
        module.external.aws_iam_users["prod_observes"].arn,
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
        module.external.aws_iam_roles["prod_makes"].arn,
        module.external.aws_iam_roles["prod_observes"].arn,
        module.external.aws_iam_users["prod_makes"].arn,
        module.external.aws_iam_users["prod_observes"].arn,
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

resource "aws_kms_key" "key-prod" {
  description             = "prod kms key for observes."
  policy                  = data.aws_iam_policy_document.key-prod.json
  deletion_window_in_days = 30
  is_enabled              = true
  enable_key_rotation     = true

  tags = {
    "Name"               = "observes-production"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

resource "aws_kms_alias" "key-prod" {
  name          = "alias/observes-prod"
  target_key_id = aws_kms_key.key-prod.key_id
}
