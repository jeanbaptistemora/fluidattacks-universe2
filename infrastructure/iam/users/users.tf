resource "aws_iam_user" "cloudwatch" {
  name = "Cloudwatch"
  path = "/"
}
resource "aws_iam_user" "fis3integration" {
  name = "FI_S3INTEGRATION"
  path = "/"
}
resource "aws_iam_user" "fluidcountconsumer" {
  name = "fluidcount_consumer"
  path = "/"
}
resource "aws_iam_user" "fluidintegratesdynamo" {
  name = "FLUIDIntegratesDynamo"
  path = "/"
}
resource "aws_iam_user" "fluidservess3" {
  name = "fluidserves_s3"
  path = "/"
}
resource "aws_iam_user" "fws3user" {
  name = "FW_S3_USER"
  path = "/"
}
