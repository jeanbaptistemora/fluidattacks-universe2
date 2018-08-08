resource "aws_iam_user" "fis3integration" {
  name = "FluidIntegrates_S3"
  path = "/"
}

resource "aws_iam_access_key" "fis3integration2" {
  user    = "${aws_iam_user.fis3integration.name}"
}

resource "aws_iam_user" "cloudwatch" {
  name = "FluidIntegrates_CloudWatch"
  path = "/"
}

resource "aws_iam_access_key" "cloudwatch2" {
  user    = "${aws_iam_user.cloudwatch.name}"
}

resource "aws_iam_user" "fluidintegratesdynamo" {
  name = "FluidIntegrates_DynamoDB"
  path = "/"
}

resource "aws_iam_access_key" "fluidintegratesdynamo2" {
  user    = "${aws_iam_user.fluidintegratesdynamo.name}"
}

resource "aws_iam_user" "fws3user" {
  name = "FluidWeb_S3"
  path = "/"
}

resource "aws_iam_access_key" "fws3user2" {
  user    = "${aws_iam_user.fws3user.name}"
}

resource "aws_iam_user" "examss3" {
  name = "FluidExams_S3"
  path = "/"
}

resource "aws_iam_access_key" "examss32" {
  user    = "${aws_iam_user.examss3.name}"
}
