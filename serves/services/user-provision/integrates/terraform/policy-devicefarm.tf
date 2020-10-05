resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-devicefarm" {
  user       = "integrates-prod"
  policy_arn = "arn:aws:iam::aws:policy/AWSDeviceFarmFullAccess"
}
