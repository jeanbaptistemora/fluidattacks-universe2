resource "aws_iam_group" "LambdaAdmins" {
  name = "LambdaAdmins"
}

resource "aws_iam_group_policy_attachment" "AWSLambdaFullAccess" {
  group      = "${aws_iam_group.LambdaAdmins.name}"
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaFullAccess"
}
