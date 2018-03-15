resource "aws_s3_bucket" "integrates_fluidattacks" {
  bucket = "fluidintegrates.fluidattacks.com"
  acl    = "private"
}
