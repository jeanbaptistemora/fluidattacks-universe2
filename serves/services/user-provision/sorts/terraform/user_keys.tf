resource "aws_iam_access_key" "sorts_prod_key_1" {
  user = "sorts_prod"
}

resource "aws_iam_access_key" "sorts_prod_key_2" {
  user = "sorts_prod"
}

resource "aws_iam_access_key" "sorts_dev_key_1" {
  user = "sorts_dev"
}

resource "aws_iam_access_key" "sorts_dev_key_2" {
  user = "sorts_dev"
}
