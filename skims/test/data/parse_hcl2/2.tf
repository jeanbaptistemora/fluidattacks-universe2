resource "aws_sqs_queue" "app_queue" {
  name = var.queue_name
  tags = var.tags
  kms_master_key_id = var.keysqs_name
  kms_data_key_reuse_period_seconds = 86400
}

resource "aws_sns_topic_subscription" "test" {
  topic_arn = "${aws_sns_topic.app_topic.arn}"
  protocol  = "sqs"
  endpoint  = "arn:aws:sqs:${var.zone}:${var.aws_account}:xxxx-${var.environment_prefix}"
  filter_policy = "{ \"scope\": [ \"SEND_TO_UI\", \"SEND_TO_ALL\" ] }"
  raw_message_delivery = true
}
