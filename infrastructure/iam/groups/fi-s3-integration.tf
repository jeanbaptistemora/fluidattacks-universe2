resource "aws_iam_group" "fis3integration" {
  name = "FI_S3INTEGRATION"
  path = "/"
}

resource "aws_iam_group_membership" "fis3integration" {
  name = "fis3integration-membership"

  users = [
    "${var.fis3integration}",
  ]

  group = "${aws_iam_group.fis3integration.name}"
}
