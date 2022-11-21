# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

variable "endpoint" {}

resource "aws_s3_bucket" "main" {
  bucket = var.endpoint

  tags = {
    "Name"               = var.endpoint
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
