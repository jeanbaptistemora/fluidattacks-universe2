resource "aws_iam_group" "web" {
  name = "FluidWeb"
  path = "/"
}

resource "aws_iam_group_membership" "web" {
  name = "web-membership"

  users = [
    "${var.fws3user}",
  ]

  group = "${aws_iam_group.web.name}"
}
