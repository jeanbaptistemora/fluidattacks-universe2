data "aws_caller_identity" "main" {}

data "aws_redshift_cluster" "observes" {
  cluster_identifier = "observes"
}

variable "redshiftUser" {}
variable "redshiftPassword" {}
variable "oktaApiToken" {}
