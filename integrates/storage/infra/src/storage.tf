variable "branch" {}

locals {
  endpoint = "integrates.${var.branch}"
  tags = {
    area = var.branch == "trunk" ? "cost" : "innovation"
  }
}

resource "aws_s3_bucket" "main" {
  bucket = local.endpoint

  tags = {
    "Name"               = local.endpoint
    "management:area"    = local.tags.area
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}
