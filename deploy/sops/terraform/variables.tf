data "aws_caller_identity" "current" {}
variable "dev_aws_access_key" {}
variable "dev_aws_secret_key" {}

variable "region" {
  default = "us-east-1"
}
