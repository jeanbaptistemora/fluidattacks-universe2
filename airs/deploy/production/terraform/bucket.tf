resource "aws_s3_bucket" "web-bucket" {
  bucket = "web.fluidattacks.com"
  acl    = "private"
  region = var.region

  website {
     index_document = "index.html"
     error_document = "error/index.html"
   }
   tags = {
    Pry = "General"
  }
}

resource "aws_s3_bucket" "bucket" {
  bucket = "fluidattacks.com"
  acl    = "private"
  region = var.region

  website {
     index_document = "index.html"
     error_document = "error/index.html"
   }
   tags = {
    Pry = "General"
  }
}
