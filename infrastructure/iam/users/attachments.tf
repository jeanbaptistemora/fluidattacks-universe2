resource "aws_iam_user_policy_attachment" "dynamo-attach" {
    user       = "${aws_iam_user.fluidintegratesdynamo.name}"
    policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_user_policy_attachment" "cloudwatch-attach" {
    user       = "${aws_iam_user.cloudwatch.name}"
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}
