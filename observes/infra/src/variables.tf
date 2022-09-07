# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

data "aws_caller_identity" "current" {}
data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "main" {
  for_each = toset([
    "observes_1",
    "observes_2",
    "observes_3",
    "observes_4",
  ])

  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = [each.key]
  }
}
