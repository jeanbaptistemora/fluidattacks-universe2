data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "region" {
  default = "us-east-1"
}

#
# Reused infrastructure from other services
#

variable "autostaling_ci_vpc_id" {
  default = "vpc-53ea4637"
}
