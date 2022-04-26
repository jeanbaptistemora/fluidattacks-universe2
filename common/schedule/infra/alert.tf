resource "aws_sns_topic" "alert" {
  name       = "schedule_alert"
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
    "Name"               = "schedule_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_sns_topic_subscription" "alert" {
  protocol  = "email"
  endpoint  = "dsalazar@fluidattacks.com"
  topic_arn = aws_sns_topic.alert.arn
}

resource "aws_cloudwatch_event_rule" "alert" {
  name = "schedule_alert"

  event_pattern = jsonencode(
    {
      source      = ["aws.ecs"]
      detail-type = ["ECS Task State Change"]
      detail = {
        clusterArn    = [aws_ecs_cluster.main.arn]
        lastStatus    = ["STOPPED"]
        stoppedReason = ["Essential container in task exited"]
        containers = {
          exitCode = [{ anything-but = 0 }]
        }
      }
    }
  )

  tags = {
    "Name"               = "schedule_alert"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_target" "alert" {
  rule      = aws_cloudwatch_event_rule.alert.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.alert.arn
}
