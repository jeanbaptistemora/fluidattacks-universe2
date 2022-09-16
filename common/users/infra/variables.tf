# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

data "aws_caller_identity" "main" {}
data "cloudflare_api_token_permission_groups" "all" {}
data "aws_eks_cluster" "common" {
  name = "common"
}
variable "region" {
  default = "us-east-1"
}
variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}
