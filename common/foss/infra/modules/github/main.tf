# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

provider "github" {
  owner = "fluidattacks"
  token = var.token
}

terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "4.20.1"
    }
  }
}
