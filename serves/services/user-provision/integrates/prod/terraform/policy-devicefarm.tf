resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-devicefarm" {
  user       = var.user-name
  policy_arn = "arn:aws:iam::aws:policy/AWSDeviceFarmFullAccess"
}
