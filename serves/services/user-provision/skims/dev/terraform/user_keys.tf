resource "aws_iam_access_key" "skims_dev_key-1" {
  user = var.user_name
}

resource "aws_iam_access_key" "skims_dev_key-2" {
  user = var.user_name
}
