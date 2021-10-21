resource "aws_iam_access_key" "_1" {
  user = var.name
}

resource "aws_iam_access_key" "_2" {
  user = var.name
}

output "keys" {
  sensitive = true

  value = {
    1 = {
      id          = aws_iam_access_key._1.id
      secret      = aws_iam_access_key._1.secret
      create_date = aws_iam_access_key._1.create_date
    }
    2 = {
      id          = aws_iam_access_key._2.id
      secret      = aws_iam_access_key._2.secret
      create_date = aws_iam_access_key._2.create_date
    }
  }
}
