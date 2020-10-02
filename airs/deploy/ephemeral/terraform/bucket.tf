resource "aws_s3_bucket" "web-ephemeral-bucket" {
  bucket = "web.eph.fluidattacks.com"
  acl    = "private"
  region = var.region

  website {
     index_document = "index.html"
     error_document = "error-index.html"
   }

  tags = {
    "Name"               = "web.eph.fluidattacks.com"
    "management:type"    = "development"
    "management:product" = "airs"
  }
}

resource "aws_s3_bucket_object" "home-index" {
  bucket       = aws_s3_bucket.web-ephemeral-bucket.id
  key          = "index.html"
  source       = "index.html"
  etag         = filemd5("index.html")
  content_type = "text/html"

  tags = {
    "Name"               = "index.html"
    "management:type"    = "development"
    "management:product" = "airs"
  }
}

resource "aws_s3_bucket_object" "error-index" {
  bucket       = aws_s3_bucket.web-ephemeral-bucket.id
  key          = "error-index.html"
  source       = "error-index.html"
  etag         = filemd5("error-index.html")
  content_type = "text/html"

  tags = {
    "Name"               = "error-index.html"
    "management:type"    = "development"
    "management:product" = "airs"
  }
}

resource "aws_s3_bucket_object" "img" {
  for_each     = {for name in fileset(path.module, "img/*"): name => name}
  bucket       = aws_s3_bucket.web-ephemeral-bucket.id
  key          = each.value
  source       = each.value
  etag         = filemd5(each.value)
  content_type = "image/png"

  tags = {
    "Name"               = each.value
    "management:type"    = "development"
    "management:product" = "airs"
  }
}

resource "aws_s3_bucket_object" "css" {
  for_each     = {for name in fileset(path.module, "css/*"): name => name}
  bucket       = aws_s3_bucket.web-ephemeral-bucket.id
  key          = each.value
  source       = each.value
  etag         = filemd5(each.value)
  content_type = "text/css"

  tags = {
    "Name"               = each.value
    "management:type"    = "development"
    "management:product" = "airs"
  }
}
