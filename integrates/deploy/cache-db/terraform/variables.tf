data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

variable "eks-subnets" {
  type = list(string)
  default = [
    "subnet-0756fc7f774c4f5de",
    "subnet-0f5137175d68f5284",
    "subnet-cd196287",
    "subnet-edb402c3",
  ]
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
