resource "aws_backup_selection" "dynamodb_daily_backup_selection" {
  iam_role_arn = aws_iam_role.integrates-backup-role.arn
  name         = "integrates_dynamodb_daily_backup_selection"
  plan_id      = aws_backup_plan.integrates_daily_backup_plan.id

  resources    = [
    for table in var.dynamodb-tables : "arn:aws:dynamodb:us-east-1:205810638802:table/${table}"
  ]
}

resource "aws_backup_selection" "dynamodb_weekly_backup_selection" {
  iam_role_arn = aws_iam_role.integrates-backup-role.arn
  name         = "integrates_dynamodb_weekly_backup_selection"
  plan_id      = aws_backup_plan.integrates_weekly_backup_plan.id

  resources    = [
    for table in var.dynamodb-tables : "arn:aws:dynamodb:us-east-1:205810638802:table/${table}"
  ]
}
