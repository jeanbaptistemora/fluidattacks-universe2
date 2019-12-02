resource "aws_sqs_queue" "integrates-queue" {
  name                      = "integrates-queue.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
  delay_seconds             = 10
  max_message_size          = 262144
  message_retention_seconds = 86400
  receive_wait_time_seconds = 20
  visibility_timeout_seconds = 360

  tags = {
    Pry = "Integrates"
  }
}

output "sqs_id" {
  value = aws_sqs_queue.integrates-queue.arn
}
