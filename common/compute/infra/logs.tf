# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_cloudwatch_log_group" "job" {
  name = "/aws/batch/job"

  tags = {
    "Name"               = "job"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_log_group" "skims" {
  name              = "skims"
  retention_in_days = 7

  tags = {
    "Name"               = "skims"
    "management:area"    = "cost"
    "management:product" = "skims"
    "management:type"    = "product"
  }
}
