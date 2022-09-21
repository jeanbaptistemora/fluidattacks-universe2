# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_sqs_queue" "celery_queue" {
  name                      = "celery"
  delay_seconds             = 5
  max_message_size          = 2048
  message_retention_seconds = 259200
  receive_wait_time_seconds = 10

  tags = {
    "Name"               = "celery"
    "Management:Area"    = "cost"
    "Management:Product" = "machine"
    "Management:Type"    = "product"
  }
}
