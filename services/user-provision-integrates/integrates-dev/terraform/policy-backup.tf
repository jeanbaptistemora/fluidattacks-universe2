resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy-backup" {
  user       = var.user-name
  policy_arn = "arn:aws:iam::aws:policy/AWSBackupOperatorAccess"
}