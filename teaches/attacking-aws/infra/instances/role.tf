resource "aws_iam_role" "ec2-role" {
  name = "Ec2Role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "instance_secure_app_attach" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess" 
  role       = aws_iam_role.ec2-role.name
}
