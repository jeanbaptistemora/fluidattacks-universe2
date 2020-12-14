resource "aws_s3_bucket" "production" {
  bucket = "front-production.fluidattacks.com"
  acl    = "private"
  region = var.region

  tags = {
    "Name"               = "front-production.fluidattacks.com"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}
