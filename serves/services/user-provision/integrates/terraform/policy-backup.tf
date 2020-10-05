resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy-backup" {
  user       = "integrates-prod"
  policy_arn = "arn:aws:iam::aws:policy/AWSBackupFullAccess"
}

resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy-backup" {
  user       = "integrates-dev"
  policy_arn = "arn:aws:iam::aws:policy/AWSBackupOperatorAccess"
}
