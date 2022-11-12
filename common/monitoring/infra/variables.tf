# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

data "aws_caller_identity" "main" {}

data "aws_redshift_cluster" "observes" {
  cluster_identifier = "observes"
}

variable "redshiftUser" {}
variable "redshiftPassword" {}
