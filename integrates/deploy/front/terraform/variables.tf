variable "aws_access_key" {}
variable "aws_secret_key" {}

data "aws_route53_zone" "fluidattacks" {
  name = "fluidattacks.com."
}

variable "region" {
  default = "us-east-1"
}

variable bucket-origin-id-development {
  default = "integrates.front.development.origin"
}

variable bucket-origin-id-production {
  default = "integrates.front.production.origin"
}
