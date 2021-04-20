data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "okta_api_token" {
  default = "Default value for tests"
}
variable "region" {
  default = "us-east-1"
}
