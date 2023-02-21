resource "aws_iam_role" "safe_role_1" {
  name = "safe_role_1"

  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        }
      }
    ]
  }
  EOF
}

resource "aws_iam_role" "vuln_role_1" {
  name = "vuln_role_1"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        NotPrincipal = {
          Servive = "ec2.amazonaws.com"
        }
      },
    ]
  })
}
