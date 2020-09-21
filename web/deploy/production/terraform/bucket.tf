resource "aws_s3_bucket" "web-bucket" {
  bucket = "web.fluidattacks.com"
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
