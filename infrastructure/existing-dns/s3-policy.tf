variable "bucket" {}
variable "bucket-integrates" {}

data "aws_s3_bucket" "b" {
  bucket = "${var.bucket}"
}


resource "aws_s3_bucket_policy" "b" {
  bucket = "${data.aws_s3_bucket.b.id}"
  policy =<<POLICY
{
      "Version": "2012-10-17",
      "Id": "Policy1513113687871",
      "Statement": [
          {
              "Sid": "Stmt1513113661499",
              "Effect": "Allow",
              "Principal": "*",
              "Action": "s3:GetObject",
              "Resource": "arn:aws:s3:::${var.bucket}/*",
              "Condition": {
                  "IpAddress": {
                      "aws:SourceIp": "${var.server}/32"
                  }
              }
          }
      ]
  }
POLICY
}


data "aws_s3_bucket" "i" {
  bucket = "${var.bucket-integrates}"
}


resource "aws_s3_bucket_policy" "i" {
  bucket = "${data.aws_s3_bucket.i.id}"
  policy =<<POLICY
{
      "Version": "2012-10-17",
      "Id": "Policy1513113687871",
      "Statement": [
          {
              "Sid": "Stmt1513113661499",
              "Effect": "Allow",
              "Principal": "*",
              "Action": "s3:GetObject",
              "Resource": "arn:aws:s3:::${var.bucket-integrates}/*",
              "Condition": {
                  "IpAddress": {
                      "aws:SourceIp": "${var.server}/32"
                  }
              }
          }
      ]
  }
POLICY
}
