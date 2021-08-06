resource "aws_iam_access_key" "skims_prod_key-1" {
  user = "skims_prod"
}

resource "aws_iam_access_key" "skims_prod_key-2" {
  user = "skims_prod"
}

resource "aws_iam_access_key" "skims_dev_key-1" {
  user = "skims_dev"
}

resource "aws_iam_access_key" "skims_dev_key-2" {
  user = "skims_dev"
}
