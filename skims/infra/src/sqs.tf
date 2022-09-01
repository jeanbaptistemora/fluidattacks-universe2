resource "aws_sqs_queue" "skims_report_queue" {
  name                      = "skims-report-queue"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10

  tags = {
    "Name"               = "skims.queue"
    "Management:Area"    = "cost"
    "Management:Product" = "skims"
    "Management:Type"    = "product"
  }
}
