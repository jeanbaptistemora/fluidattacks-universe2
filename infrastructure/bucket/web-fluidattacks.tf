variable "webBucket" {}

resource "aws_s3_bucket" "web_fluidattacks" {
  bucket = "${var.webBucket}"
  acl    = "private"

  website {
     index_document = "index.html"
     error_document = "web/en/error/index.html"
   }
   tags {
    Pry = "General"
  }
}

output "webName" {
  value = "${aws_s3_bucket.web_fluidattacks.id}"

}
