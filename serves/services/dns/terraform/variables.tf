variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "elbDns" {}
variable "elbZone" {}

variable "s3-east-1-zone-id" {
  default = "Z3AQBSTGFYJSTF"
}
variable "domain" {
  default = "fluidattacks.com"
}
variable "region" {
  default = "us-east-1"
}
variable "secDomains" {
  type = list(string)
  default = [
    "fluid.com.co",
    "fluidsignal.co",
    "fluidsignal.com.co",
    "fluidsignal.com",
    "fluid.la",
    "fluidattacks.co",
    "fluidattacks.com.co",
    "fluidattacks.io"
  ]
}
