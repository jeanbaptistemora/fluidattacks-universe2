variable "fwBucket" {}
variable "fiS3Arn" {}

data "aws_s3_bucket" "b" {
  bucket = var.fwBucket
}

resource "aws_s3_bucket_policy" "b" {
  bucket = data.aws_s3_bucket.b.id
  policy = <<POLICY
{
      "Version": "2012-10-17",
      "Id": "Policy1513113687871",
      "Statement": [
          {
              "Sid": "Stmt1513113661499",
              "Effect": "Allow",
              "Principal": "*",
              "Action": ["s3:GetObject",
                  "s3:ListBucket"
              ],
              "Resource": ["arn:aws:s3:::${var.fwBucket}/*",
                  "arn:aws:s3:::${var.fwBucket}"
              ]
          }
      ]
  }
POLICY

}
