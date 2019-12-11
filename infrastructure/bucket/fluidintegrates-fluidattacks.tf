variable "fiBucket" {}

resource "aws_s3_bucket" "integrates_fluidattacks" {
  bucket = var.fiBucket
  acl    = "private"
}

output "fiName" {
  value = aws_s3_bucket.integrates_fluidattacks.id

}
