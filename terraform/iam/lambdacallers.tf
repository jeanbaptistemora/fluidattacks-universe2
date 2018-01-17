resource "aws_iam_group" "LambdaCallers" {
  name = "LambdaCallers"
}

resource "aws_iam_group_policy_attachment" "AWSLambdaDynamoDBExecutionRole" {
  group      = "${aws_iam_group.LambdaCallers.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaDynamoDBExecutionRole"
}

resource "aws_iam_group_policy_attachment" "attach" {
  group      = "${aws_iam_group.LambdaCallers.name}"
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaExecute"
}

resource "aws_iam_group_policy_attachment" "AWSLambdaBasicExecutionRole" {
  group      = "${aws_iam_group.LambdaCallers.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_group_policy_attachment" "AWSLambdaInvocation-DynamoDB" {
  group      = "${aws_iam_group.LambdaCallers.name}"
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaInvocation-DynamoDB"
}

resource "aws_iam_group_policy_attachment" "CloudFormation_Lambda" {
  group      = "${aws_iam_group.LambdaCallers.name}"
  policy_arn = "${aws_iam_policy.CloudFormation_Lambda.arn}"
}
