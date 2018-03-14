resource "aws_iam_user_policy_attachment" "dynamo-attach" {
    user       = "${aws_iam_user.fluidintegratesdynamo.name}"
    policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_group_membership" "cloudwatch" {
  name = "cloudwatch-group-membership"

  users = [
    "${aws_iam_user.cloudwatch.name}"
  ]

  group = "CloudWatch"
}
