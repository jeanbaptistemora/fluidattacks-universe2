resource "aws_iam_group" "fluidserves" {
  name = "FluidServes"
  path = "/"
}

resource "aws_iam_group_membership" "fluidserves" {
  name = "fluidserves-membership"

  users = [
    "${var.examss3}"
  ]

  group = "${aws_iam_group.fluidserves.name}"
}
