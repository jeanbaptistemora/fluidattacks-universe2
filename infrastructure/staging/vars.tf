#AWA Variables
variable "aws_innovation_access_key" {}
variable "aws_innovation_secret_key" {}
variable "region" {}

#Network Variables
variable "cidr" {}

#DB Variables
variable "dbRegion" {}
variable "storageType" {}
variable "engine" {}
variable "engineVersion" {}
variable "instanceClass" {}
variable "dbDevName" {}
variable "dbDevUser" {}
variable "dbDevPass" {}
variable "dbZones" {
  type = list(string)
  default = [
    "us-east-1a",
    "us-east-1b",
    "us-east-1c",
    "us-east-1d",
    "us-east-1e",
  ]
}
