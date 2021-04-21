data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "okta_api_token" {}
variable "okta_users" {}
variable "okta_groups" {}
variable "region" {
  default = "us-east-1"
}
