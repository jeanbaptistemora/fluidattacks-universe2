# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

variable "region" {
  default = "us-east-1"
}

variable "secure-app-vpc-id" {
  default = "vpc-f0f20d8d"
}

variable "intranet-vpc-id" {
  default = "vpc-0eeec8817486ada10"
}
