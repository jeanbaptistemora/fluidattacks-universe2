resource "aws_iam_user" "fis3integration" {
  name = "FI_S3INTEGRATION"
  path = "/"
}

resource "aws_iam_access_key" "fis3integration" {
  user    = "${aws_iam_user.fis3integration.name}"
}

resource "aws_iam_user" "cloudwatch" {
  name = "Cloudwatch"
  path = "/"
}

resource "aws_iam_access_key" "cloudwatch" {
  user    = "${aws_iam_user.cloudwatch.name}"
}

resource "aws_iam_user" "fluidintegratesdynamo" {
  name = "FLUIDIntegratesDynamo"
  path = "/"
}

resource "aws_iam_access_key" "fluidintegratesdynamo" {
  user    = "${aws_iam_user.fluidintegratesdynamo.name}"
}

resource "aws_iam_user" "fws3user" {
  name = "FW_S3_USER"
  path = "/"
}

resource "aws_iam_access_key" "fws3user" {
  user    = "${aws_iam_user.fws3user.name}"
}

resource "aws_iam_user" "examss3" {
  name = "FS_EXAMS_S3"
  path = "/"
}

resource "aws_iam_access_key" "examss3" {
  user    = "${aws_iam_user.examss3.name}"
}
