data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

data "aws_route53_zone" "fluidattacks" {
  name = "fluidattacks.com."
}

variable "region" {
  default = "us-east-1"
}

variable "user-name" {
  default = "integrates-dev"
}
