variable "aws_s3_analytics_bucket" {
  type    = string
  default = "fluidintegrates.analytics"
}

variable "aws_s3_evidences_bucket" {
  type    = string
  default = "fluidintegrates.evidences"
}

variable "aws_s3_resources_bucket" {
  type    = string
  default = "fluidintegrates.resources"
}

variable "aws_s3_reports_bucket" {
  type    = string
  default = "fluidintegrates.reports"
}

variable "aws_s3_build_bucket" {
  type    = string
  default = "fluidintegrates.build"
}

variable "aws_s3_forces_bucket" {
  type    = string
  default = "fluidintegrates.forces"
}
