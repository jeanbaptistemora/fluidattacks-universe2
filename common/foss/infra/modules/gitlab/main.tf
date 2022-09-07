# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

provider "gitlab" {
  token = var.token
}

terraform {
  required_providers {
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = "3.12.0"
    }
  }
}
