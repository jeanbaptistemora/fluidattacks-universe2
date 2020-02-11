resource "aws_backup_selection" "dynamodb_backup_selection" {
  iam_role_arn = "arn:aws:iam::294474830922:role/service-role/AWSBackupDefaultServiceRole"
  name         = "integrates_dynamodb_backup_selection"
  plan_id      = aws_backup_plan.integrates_backup_plan.id

  resources = [
    "arn:aws:dynamodb:us-east-1:205810638802:table/FI_alerts_by_company"
  ]
}