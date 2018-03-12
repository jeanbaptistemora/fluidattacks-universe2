resource "aws_iam_group" "lambdacallers" {
  name = "LambdaCallers"
  path = "/"
}

resource "aws_iam_group_membership" "lambdacallers" {
  name = "lambdacallers-membership"

  users = [
    "fluidcount_consumer",
  ]

  group = "${aws_iam_group.lambdacallers.name}"
}
