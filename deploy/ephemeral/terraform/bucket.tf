resource "aws_s3_bucket" "web-ephemeral-bucket" {
  bucket = "web.eph.fluidattacks.com"
  acl    = "private"
  region = var.region

  website {
     index_document = "index.html"
     error_document = "index-error.html"
   }
   tags = {
    Pry = "General"
  }
}

resource "aws_s3_bucket_object" "home-index" {
  bucket       = aws_s3_bucket.web-ephemeral-bucket.id
  key          = "index.html"
  source       = "index.html"
  content_type = "text/html"
}

resource "aws_s3_bucket_object" "error-index" {
  bucket       = aws_s3_bucket.web-ephemeral-bucket.id
  key          = "index-error.html"
  source       = "index-error.html"
  content_type = "text/html"
}
