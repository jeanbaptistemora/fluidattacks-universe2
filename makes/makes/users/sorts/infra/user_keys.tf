resource "aws_iam_access_key" "sorts_prod_key-1" {
  user = "sorts_prod"
}

resource "aws_iam_access_key" "sorts_prod_key-2" {
  user = "sorts_prod"
}

resource "aws_iam_access_key" "sorts_dev_key-1" {
  user = "sorts_dev"
}

resource "aws_iam_access_key" "sorts_dev_key-2" {
  user = "sorts_dev"
}
