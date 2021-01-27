data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

variable "fluid_vpc_id" {
  default = "vpc-0ea1c7bd6be683d2d"
}

variable "subnets" {
  type = list(string)
  default = [
    "subnet-0ac02a346bceef9ad",
    "subnet-0996b60804976732b",
    "subnet-07f62937237940742",
  ]
}

variable "region" {
  default = "us-east-1"
}
