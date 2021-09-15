terraform {
  required_version = "~> 0.14.0"

  required_providers {
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = "3.7.0"
    }
  }
}

variable "gitlab_token" {}
variable "key_1" {}
variable "key_2" {}
variable "prefix" {}
variable "protected" {}
variable "project_id" {
  default = "20741933" # product
}

provider "gitlab" {
  token = var.gitlab_token
}


resource "time_static" "key_1_created_at" {
  rfc3339 = var.key_1.create_date
}

resource "time_static" "key_2_created_at" {
  rfc3339 = var.key_2.create_date
}

resource "gitlab_project_variable" "key_id" {
  key       = "${var.prefix}_AWS_ACCESS_KEY_ID"
  masked    = true
  project   = var.project_id
  protected = var.protected
  value = (
    time_static.key_1_created_at.unix > time_static.key_2_created_at.unix
    ? var.key_1.id
    : var.key_2.id
  )
}

resource "gitlab_project_variable" "key_secret" {
  key       = "${var.prefix}_AWS_SECRET_ACCESS_KEY"
  masked    = true
  project   = var.project_id
  protected = var.protected
  value = (
    time_static.key_1_created_at.unix > time_static.key_2_created_at.unix
    ? var.key_1.secret
    : var.key_2.secret
  )
}
