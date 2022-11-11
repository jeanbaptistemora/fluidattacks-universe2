# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

data "aws_caller_identity" "main" {}
variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}


# Reused infrastructure

data "aws_iam_role" "main" {
  for_each = toset([
    "dev",
    "prod_airs",
    "prod_common",
    "prod_docs",
    "prod_forces",
    "prod_integrates",
    "prod_melts",
    "prod_observes",
    "prod_skims",
    "prod_sorts",
  ])

  name = each.key
}
data "aws_iam_instance_profile" "main" {
  for_each = toset([
    "ecsInstanceRole",
  ])

  name = each.key
}
data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "batch_clone" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["batch_clone"]
  }
}
data "aws_subnet" "batch_main" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["batch_main"]
  }
}
