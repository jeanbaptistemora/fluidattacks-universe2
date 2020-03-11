variable "aws_access_key" {}
variable "aws_secret_key" {}

data "aws_route53_zone" "fluidattacks" {
  name = "fluidattacks.com."
}

variable bucket-origin-id {
  default = "web-ephemeral-bucket-origin"
}

variable "region" {
  default = "us-east-1"
}
