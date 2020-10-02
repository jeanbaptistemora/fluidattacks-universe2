resource "aws_s3_bucket" "bucket" {
  bucket = "fluidattacks.com"
  acl    = "private"
  region = var.region

  website {
    index_document = "index.html"
    error_document = "error/index.html"
  }

  tags = {
    "Name"               = "fluidattacks.com"
    "management:type"    = "production"
    "management:product" = "airs"
  }
}
