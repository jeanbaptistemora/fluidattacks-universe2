resource "aws_instance" "i-0d1583d0c02a9bb47" {
  ami                         = "ami-04b9e92b5572fa0d1"
  availability_zone           = "us-east-1a"
  ebs_optimized               = false
  instance_type               = "t2.small"
  monitoring                  = false
  key_name                    = "generic_aws_key"
  subnet_id                   = "subnet-00f969b107a8e55b4"
  vpc_security_group_ids      = ["sg-0f98371a3f6cad87e"]
  associate_public_ip_address = true
  private_ip                  = "10.0.0.44"
  source_dest_check           = true

  root_block_device {
    volume_type           = "gp2"
    volume_size           = 20
    delete_on_termination = true
    encrypted = false
  }

  ebs_block_device {
    device_name           = "/dev/sdg"
    volume_type           = "gp2"
    volume_size           = 20
    delete_on_termination = true
    encrypted = false
  }

  tags = {
    method  = "aws.ec2.has_unencrypted_volumes"
    Name    = "aws.ec2_unencrypted"
  }
}

resource "aws_ebs_encryption_by_default" "example" {
  enabled = false
}

resource "aws_security_group" "allow_tls" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"
  vpc_id      = "someid"

  ingress {
    # TLS (change to whatever ports you need)
    from_port   = 443
    to_port     = 446
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    method  = "aws.terraform.ec2.allows_all_outbound_traffic"
    Name    = "aws.terraform.allows_all_outbound_traffic"
  }
}

resource "aws_security_group_rule" "allow_all" {
  security_group_id = "sg-123456"
  type            = "ingress"
  from_port       = 0
  to_port         = 65535
  protocol        = "-1"
  cidr_blocks = "0.0.0.0/0"
  prefix_list_ids = ["pl-12c4e678"]

}

resource "aws_iam_policy" "policy1" {
  name        = "test_policy"
  path        = "/"
  description = "My test policy"

  policy = <<EOF
{
  "Statement": [
    {
      "Action": [
        "ecr:*"
      ],
      "Effect": "Allow",
      "Resource": [
        "*"
      ]
    },
    {
      "Action": "ecr:*",
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "NotAction": []
    },
    {
      "Effect": "Allow",
      "NotResource": []
    }
  ],
  "Version": "2012-10-17"
}
EOF
}

resource "aws_iam_role" "test_role" {
  name = "test_role"

  assume_role_policy = <<-EOF
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

resource "aws_iam_role_policy" "policy2" {
  name        = "test_policy_2"
  path        = "/"
  description = "Another test policy"
  role = aws_iam_role.test_role.id

  policy = <<EOF
{
  "Statement": [
    {
      "Action": "*",
      "Effect": "Deny",
      "Resource": "*"
    },
    {
      "Action": [
        "ecr:Get*"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:ecr:us-east-1::repository/*"
      ]
    }
  ],
  "Version": "2012-10-17"
}
EOF
}

resource "aws_iam_user_policy" "lb_ro" {
  name = "test"
  user = "${aws_iam_user.lb.name}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "ec2:Describe*"
      ],
      "Effect": "Deny",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_user" "lb" {
  name = "loadbalancer"
  path = "/system/"
}

resource "aws_iam_access_key" "lb" {
  user = "${aws_iam_user.lb.name}"
}

resource "aws_db_instance" "default" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "foo"
  password             = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
}

resource "aws_db_instance" "default" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "foo"
  password             = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
}

resource "aws_rds_cluster" "default" {
  cluster_identifier      = "aurora-cluster-demo"
  engine                  = "aurora-mysql"
  engine_version          = "5.7.mysql_aurora.2.03.2"
  availability_zones      = ["us-west-2a", "us-west-2b", "us-west-2c"]
  database_name           = "mydb"
  master_username         = "foo"
  master_password         = "bar"
  backup_retention_period = 5
  preferred_backup_window = "07:00-09:00"
  deletion_protection  = "false"
}
