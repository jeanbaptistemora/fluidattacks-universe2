resource "aws_iam_group" "web" {
  name = "web"
  path = "/"
}

resource "aws_iam_group_membership" "web" {
  name = "web-membership"

  users = [
    "FW_S3_USER",
  ]

  group = "${aws_iam_group.web.name}"
}
