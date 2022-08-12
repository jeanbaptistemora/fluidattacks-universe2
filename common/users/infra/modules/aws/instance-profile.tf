resource "aws_iam_instance_profile" "main" {
  name = var.name
  role = aws_iam_role.main.name
}
