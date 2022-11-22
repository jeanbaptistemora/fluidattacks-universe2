# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

variable "branch" {}

locals {
  endpoint = var.branch == "trunk" ? "prod.integrates" : "${var.branch}.integrates"
  tags = {
    area = var.branch == "trunk" ? "cost" : "innovation"
  }
}

resource "aws_s3_bucket" "main" {
  bucket = local.endpoint

  tags = {
    "Name"               = local.endpoint
    "management:area"    = local.tags.area
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
