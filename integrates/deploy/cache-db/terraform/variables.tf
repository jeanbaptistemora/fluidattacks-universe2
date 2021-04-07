data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

variable "fluid_vpc_id" {
  default = "vpc-0ea1c7bd6be683d2d"
}

variable "subnets" {
  type = list(string)
  default = [
    "subnet-0df4178d0c9354aad",
    "subnet-0412793dec0eddea9",
    "subnet-08849bfa044faf25a",
  ]
}

variable "region" {
  default = "us-east-1"
}
