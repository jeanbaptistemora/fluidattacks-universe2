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
