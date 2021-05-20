variable "aws_iam_users" {
  type    = list(string)
  default = []
}

data "aws_iam_user" "aws_iam_users" {
  for_each  = toset(var.aws_iam_users)
  user_name = each.value
}

output "aws_iam_users" {
  value = data.aws_iam_user.aws_iam_users
}
