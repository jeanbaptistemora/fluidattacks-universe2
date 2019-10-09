data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

variable "onelogin-account-id" {
  default = "842984801698"
}

variable "onelogin-external-id" {
  default = "AC84IJCC58FHC3"
}

variable "region" {
  default = "us-east-1"
}
