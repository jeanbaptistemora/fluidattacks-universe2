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
  default = "integrates-prod"
}

variable "terraform_state_lock_arn" {
  default = "arn:aws:dynamodb:us-east-1:205810638802:table/terraform_state_lock"
}
