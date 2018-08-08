resource "aws_iam_group" "fis3integration" {
  name = "FluidIntegrates_S3"
  path = "/"
}

resource "aws_iam_group_membership" "fis3integration" {
  name = "fis3integration-membership"

  users = [
    "${var.fis3integration}",
  ]

  group = "${aws_iam_group.fis3integration.name}"
}
