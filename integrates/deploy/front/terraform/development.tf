resource "aws_s3_bucket" "development" {
  bucket = "front-development.fluidattacks.com"
  acl    = "private"
  region = var.region

  tags = {
    "Name"               = "front-development.fluidattacks.com"
    "management:type"    = "development"
    "management:product" = "integrates"
  }
}
