# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
