resource "aws_iam_access_key" "forces_prod_key-1" {
  user = "forces_prod"
}

resource "aws_iam_access_key" "forces_dev_key-1" {
  user = "forces_dev"
}
