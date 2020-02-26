data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "db_user" {}
variable "db_password" {}

variable "region" {
  default = "us-east-1"
}

variable "fluid-vpc-id" {
  default = "vpc-0ea1c7bd6be683d2d"
}
