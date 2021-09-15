resource "aws_iam_user_policy_attachment" "continuous-prod-attach-policy-dynamodb" {
  user       = "continuous-prod"
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}
