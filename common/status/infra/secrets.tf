# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

variable "accountId" {
  sensitive = true
}
variable "alertSms" {
  type = string
}
variable "alertUsers" {
  type = list(string)
}
variable "apiKey" {
  sensitive = true
}
variable "envBitBucketPwd" {
  sensitive = true
}
variable "envBitBucketUser" {
  sensitive = true
}
variable "envIntegratesApiToken" {
  sensitive = true
}
