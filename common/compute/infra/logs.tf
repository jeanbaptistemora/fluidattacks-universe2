# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_cloudwatch_log_group" "job" {
  name = "/aws/batch/job"

  tags = {
    "Name"               = "job"
    "Management:Area"    = "cost"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}

resource "aws_cloudwatch_log_group" "skims" {
  name = "skims"

  tags = {
    "Name"               = "skims"
    "Management:Area"    = "cost"
    "Management:Product" = "skims"
    "Management:Type"    = "product"
  }
}
