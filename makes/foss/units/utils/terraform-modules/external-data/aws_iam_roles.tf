
variable "aws_iam_roles" {
  type    = list(string)
  default = []
}

data "aws_iam_role" "aws_iam_roles" {
  for_each = toset(var.aws_iam_roles)
  name     = each.value
}

output "aws_iam_roles" {
  value = data.aws_iam_role.aws_iam_roles
}
