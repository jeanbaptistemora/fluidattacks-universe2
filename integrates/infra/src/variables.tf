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
    "k8s_1",
    "k8s_2",
    "k8s_3",
  ])

  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = [each.key]
  }
}
data "cloudflare_zones" "fluidattacks_com" {
  filter {
    name = "fluidattacks.com"
  }
}
data "cloudflare_ip_ranges" "cloudflare" {}

variable "cloudflare_api_token" {}
variable "twilio_account_sid" {}
variable "twilio_auth_token" {}
variable "region" {
  default = "us-east-1"
}
