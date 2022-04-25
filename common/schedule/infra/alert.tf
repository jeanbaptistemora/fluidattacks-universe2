resource "aws_sns_topic" "alert" {
  name              = "schedule_alert"
  fifo_topic        = false
  kms_master_key_id = "alias/aws/sns"

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
        lastStatus    = ["STOPPED"]
        stoppedReason = ["Essential container in task exited"]
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
