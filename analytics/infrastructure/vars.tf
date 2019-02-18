terraform {
  required_version = ">= 0.11, < 0.12"
}
variable "name_prefix" {
  default = "analytics"
  description = "Analytics environment."
}
variable "aws_region" {
  default = "us-east-1"
  description = "AWS region."
}
provider "aws" {
  region = "${var.aws_region}"
}
