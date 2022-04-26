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
  endpoint  = "development@fluidattacks.com"
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

  input_transformer {
    input_paths = {
      startedBy = "$.detail.startedBy"
      taskArn   = "$.detail.taskArn"
      startedAt = "$.detail.startedAt"
      stoppedAt = "$.detail.stoppedAt"
    }
    input_template = <<-EOF
      {
        "reason": "Schedule container finished with failed exit code",
        "schedule": <startedBy>,
        "taskArn": <taskArn>,
        "startedAt": <startedAt>,
        "stoppedAt": <stoppedAt>,
        "urls": "You can access the following urls by replacing {{taskId}} with the ID in {{taskArn}}",
        "taskUrl": "https://us-east-1.console.aws.amazon.com/ecs/home?region=us-east-1#/clusters/schedule/tasks/{{taskId}}/details",
        "logsUrl": "https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/schedule/log-events/schedule$252Fmakes$252F{{taskId}}"
      }
    EOF
  }
}
