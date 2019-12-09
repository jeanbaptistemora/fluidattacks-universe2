data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

variable "break_build_projects" {
  type = list(string)
}
variable "break_build_project_allies" {
  type = map(list(string))
}
variable "break-build-bucket" {
  default = "break-build-logs"
}
variable "region" {
  default = "us-east-1"
}
