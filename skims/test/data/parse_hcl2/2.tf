resource "aws_sqs_queue" "app_queue" {
  name = var.queue_name
  tags = var.tags
  kms_master_key_id = var.keysqs_name
  kms_data_key_reuse_period_seconds = 86400
}
