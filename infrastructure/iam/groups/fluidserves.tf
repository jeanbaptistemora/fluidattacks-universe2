resource "aws_iam_group" "fluidserves" {
  name = "fluidserves"
  path = "/"
}

resource "aws_iam_group_membership" "fluidserves" {
  name = "fluidserves-membership"

  users = [
    "fluidserves_s3",
  ]

  group = "${aws_iam_group.fluidserves.name}"
}
