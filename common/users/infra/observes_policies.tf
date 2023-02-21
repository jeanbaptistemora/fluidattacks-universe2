resource "aws_iam_policy" "observes_kinesis_infra_management" {
  name = "observes_kinesis_infra_management"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "KinesisInfraManagement"
        Effect = "Allow"
        Action = [
          "kinesis:AddTagsToStream",
          "kinesis:CreateStream",
          "kinesis:DeleteStream",
          "kinesis:DecreaseStreamRetentionPeriod",
          "kinesis:DeregisterStreamConsumer",
          "kinesis:DisableEnhancedMonitoring",
          "kinesis:EnableEnhancedMonitoring",
          "kinesis:GetRecords",
          "kinesis:GetShardIterator",
          "kinesis:IncreaseStreamRetentionPeriod",
          "kinesis:MergeShards",
          "kinesis:RegisterStreamConsumer",
          "kinesis:RemoveTagsFromStream",
          "kinesis:SplitShard",
          "kinesis:StartStreamEncryption",
          "kinesis:StopStreamEncryption",
          "kinesis:SubscribeToShard",
          "kinesis:UpdateShardCount",
          "kinesis:UpdateStreamMode",
        ]
        Resource = [
          "arn:aws:kinesis:${var.region}:${data.aws_caller_identity.main.account_id}:stream/observes-mirror"
        ]
      },
    ]
  })
  tags = {
    "Name"               = "observes_kinesis_infra_management"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_iam_policy" "observes_kinesis_infra_read" {
  name = "observes_kinesis_infra_read"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "KinesisInfraManagement"
        Effect = "Allow"
        Action = [
          "kinesis:Describe*",
          "kinesis:List*",
        ]
        Resource = [
          "arn:aws:kinesis:${var.region}:${data.aws_caller_identity.main.account_id}:stream/observes-mirror"
        ]
      },
    ]
  })
  tags = {
    "Name"               = "observes_kinesis_infra_read"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}
