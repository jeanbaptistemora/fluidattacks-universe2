resource "aws_s3_bucket" "web_fluidattacks" {
  bucket = "web.fluidattacks.com"
  acl    = "private"

  website {
     index_document = "index.html"
     error_document = "web/en/error/index.html"
   }
   tags {
    Pry = "General"
  }
}
