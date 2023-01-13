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
  endpoint  = "development@fluidattacks.com"
  topic_arn = aws_sns_topic.main.arn
}

resource "aws_cloudwatch_event_rule" "alert" {
  name = "compute_alert"

  event_pattern = jsonencode({
    source      = ["aws.batch"]
    detail-type = ["Batch Job State Change"]
    detail = {
      status = ["FAILED"]
      containerReason = [
        { anything-but = { prefix = "CannotInspectContainerError" } },
        { exists = false }
      ],
    }
  })

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
      containerReason = "$.detail.container.reason"
      jobId           = "$.detail.jobId"
      jobName         = "$.detail.jobName"
      jobQueue        = "$.detail.jobQueue"
      status          = "$.detail.status"
      statusReason    = "$.detail.statusReason"
    }
    input_template = <<-EOF
      {
        "jobName": <jobName>,
        "jobQueue": <jobQueue>,
        "jobUrl": "https://us-east-1.console.aws.amazon.com/batch/home?region=us-east-1#jobs/detail/<jobId>",
        "status": <status>,
        "statusReason": <statusReason>,
        "containerReason": <containerReason>
      }
    EOF
  }
}
