resource "aws_iam_role" "integrates-backup-role" {
  name               = "integrates-backup"
  assume_role_policy = data.aws_iam_policy_document.backup-assume-role-policy-data.json

  tags = {
    "Name"            = "integrates-backup"
    "management:area" = "cost"
    "management:type" = "product"
  }
}

resource "aws_iam_role_policy_attachment" "integrates-backup-policy-backup" {
  role       = aws_iam_role.integrates-backup-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

resource "aws_iam_role_policy_attachment" "integrates-backup-policy-restore" {
  role       = aws_iam_role.integrates-backup-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForRestores"
}
