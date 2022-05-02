resource "aws_sns_topic" "main" {
  name       = "compute_alert"
  fifo_topic = false

  policy = jsonencode(
    {
      Version = "2008-10-17"
      Statement = [
        {
          Sid    = "default"
          Effect = "Allow"
          Principal = {
            AWS = "*"
          }
          Action = [
            "sns:GetTopicAttributes",
            "sns:SetTopicAttributes",
            "sns:AddPermission",
            "sns:RemovePermission",
            "sns:DeleteTopic",
            "sns:Subscribe",
            "sns:ListSubscriptionsByTopic",
            "sns:Publish",
          ]
          Resource = ["*"]
          Condition = {
            StringEquals = {
              "AWS:SourceOwner" = "205810638802"
            }
          }
        },
        {
          Sid    = "eventsSns",
          Effect = "Allow",
          Principal = {
            Service = ["events.amazonaws.com"]
          },
          Action   = ["sns:Publish"]
          Resource = ["*"]
        },
      ]
    }
  )

  tags = {
    "Name"               = "compute_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_sns_topic_subscription" "main" {
  protocol  = "email"
  endpoint  = "dsalazar@fluidattacks.com"
  topic_arn = aws_sns_topic.main.arn
}

resource "aws_cloudwatch_event_rule" "alert" {
  name = "compute_alert"

  event_pattern = jsonencode(
    {
      source      = ["aws.batch"]
      detail-type = ["Batch Job State Change"]
      detail = {
        status = ["FAILED"]
        container = {
          exitCode = [{ anything-but = 0 }]
        }
      }
    }
  )

  tags = {
    "Name"               = "compute_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_target" "alert" {
  rule      = aws_cloudwatch_event_rule.alert.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.main.arn

  input_transformer {
    input_paths = {
      createdAt    = "$.detail.createdAt"
      jobArn       = "$.detail.jobArn"
      jobName      = "$.detail.jobName"
      jobQueue     = "$.detail.jobQueue"
      startedAt    = "$.detail.startedAt"
      stoppedAt    = "$.detail.stoppedAt"
      status       = "$.detail.status"
      statusReason = "$.detail.statusReason"
    }
    input_template = <<-EOF
      {
        "jobName": <jobName>,
        "jobArn": <jobArn>,
        "jobQueue": <jobQueue>,
        "status": <status>,
        "statusReason": <statusReason>,
        "createdAt": <createdAt>,
        "startedAt": <startedAt>,
        "stoppedAt": <stoppedAt>,
        "urls": "You can access the following urls by replacing {{jobId}} with the ID in {{jobArn}}",
        "jobUrl": "https://us-east-1.console.aws.amazon.com/batch/home?region=us-east-1#jobs/detail/{{jobId}}"
      }
    EOF
  }
}
