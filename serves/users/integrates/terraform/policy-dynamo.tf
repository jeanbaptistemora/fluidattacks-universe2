resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-dynamodb" {
  user       = "integrates-prod"
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy-dynamo" {
  user       = "integrates-dev"
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}
