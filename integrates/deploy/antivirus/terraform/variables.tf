variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "region" {
  default = "us-east-1"
}

variable "aws_s3_antivirus_bucket" {
  type    = string
  default = "fluidintegrates.antivirus"
}
