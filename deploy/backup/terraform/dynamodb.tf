resource "aws_backup_selection" "dynamodb_backup_selection" {
  iam_role_arn = aws_iam_role.integrates-backup-role.arn
  name         = "integrates_dynamodb_backup_selection"
  plan_id      = aws_backup_plan.integrates_backup_plan.id

  resources = [
    "arn:aws:dynamodb:us-east-1:205810638802:table/FI_alerts_by_company"
  ]
}
