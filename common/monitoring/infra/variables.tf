# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

data "aws_caller_identity" "main" {}
data "aws_redshift_cluster" "observes" {
  cluster_identifier = "observes"
}
data "aws_dynamodb_table" "terraform_state_lock" {
  name = "terraform_state_lock"
}

# variable "terraform_state_lock_arn" {
#   default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
# }

variable "redshiftUser" {}
variable "redshiftPassword" {}
