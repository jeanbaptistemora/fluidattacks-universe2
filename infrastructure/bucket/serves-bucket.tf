variable "bucketName" {}

resource "aws_s3_bucket" "serves_bucket" {
  bucket = "${var.bucketName}"
  acl    = "private"
}
