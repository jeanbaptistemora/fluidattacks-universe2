data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "gitlab_token" {}

variable "region" {
  default = "us-east-1"
}
