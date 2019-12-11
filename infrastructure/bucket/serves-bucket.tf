variable "fsBucket" {}

resource "aws_s3_bucket" "serves_bucket" {
  bucket = var.fsBucket
  acl    = "private"
}
