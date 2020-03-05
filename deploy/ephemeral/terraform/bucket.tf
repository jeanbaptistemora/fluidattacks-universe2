resource "aws_s3_bucket" "web-ephemeral-bucket" {
  bucket = "web.eph.fluidattacks.com"
  acl    = "private"
  region = var.region

  website {
     index_document = "index.html"
     error_document = "web/error/index.html"
   }
   tags = {
    Pry = "General"
  }
}
