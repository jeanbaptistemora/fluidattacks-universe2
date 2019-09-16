# This file creates a bucket to store tfstate json files for all
# our services

variable "fluidattacks-terraform-states-bucket" {}

resource "aws_s3_bucket" "fluidattacks-terraform-states-bucket" {
  bucket = var.fluidattacks-terraform-states-bucket
  region = var.region
  acl    = "private"
  versioning {
    enabled = true
  }

  # Enable server-side encryption by default
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
