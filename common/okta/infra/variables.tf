# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

data "aws_caller_identity" "current" {}
data "okta_group" "everyone" {
  name = "Everyone"
}
variable "oktaApiToken" {}

variable "oktaDataApps" {}
variable "oktaDataGroups" {}
variable "oktaDataRules" {}
variable "oktaDataUsers" {}
variable "oktaDataAppGroups" {}
variable "oktaDataAppUsers" {}
variable "oktaDataAwsGroupRoles" {}
variable "oktaDataAwsUserRoles" {}
