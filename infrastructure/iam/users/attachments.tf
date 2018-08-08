resource "aws_iam_group_membership" "cloudwatch" {
  name = "cloudwatch-group-membership"

  users = [
    "${aws_iam_user.cloudwatch.name}"
  ]

  group = "CloudWatch"
}
