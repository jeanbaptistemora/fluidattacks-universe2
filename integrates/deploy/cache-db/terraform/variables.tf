data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

data "aws_iam_role" "dax_role" {
  name = "DaxtoDynamoDB"
}

variable "subnets" {
  type = list(string)
  default = [
    "subnet-0ac02a346bceef9ad",
    "subnet-0996b60804976732b",
    "subnet-07f62937237940742",
  ]
}

variable "security_groups"{
  type = list(string)
  default = [
    "sg-00b14fffdfb71a20c"
  ]
}

variable "region" {
  default = "us-east-1"
}
