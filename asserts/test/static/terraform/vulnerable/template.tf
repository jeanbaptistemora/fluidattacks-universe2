resource "aws_security_group" "allow_tls" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"
  vpc_id      = "someid"

  ingress {
    # TLS (change to whatever ports you need)
    from_port        = 443
    to_port          = 446
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    method = "aws.terraform.ec2.allows_all_outbound_traffic"
    Name   = "aws.terraform.allows_all_outbound_traffic"
  }
}

resource "aws_security_group_rule" "allow_all" {
  security_group_id = "sg-123456"
  type              = "ingress"
  from_port         = 0
  to_port           = 65535
  protocol          = "-1"
  cidr_blocks       = "0.0.0.0/0"
  prefix_list_ids   = ["pl-12c4e678"]

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
      "Action": "logs:*",
      "Effect": "Allow",
      "Resource": "arn:aws:logs:*:*:*:*"
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
  role        = aws_iam_role.test_role.id

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

resource "aws_iam_role_policy" "policy_iam_powers" {
  name        = "policy_iam_powers"
  path        = "/"
  description = "Test policy with IAM powers"
  role        = aws_iam_role.test_role.id

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
    "Action": "iam:ListUsers",
    "Effect": "Allow",
    "Resource": "*"
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

resource "aws_iam_user_policy" "lb_ro" {
  name = "test"
  user = aws_iam_user.lb.name

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
  user = aws_iam_user.lb.name
}

resource "aws_launch_template" "foo" {
  name = "foo"

  block_device_mappings {
    device_name = "/dev/sda1"

    ebs {
      volume_size = 20
    }
  }

  capacity_reservation_specification {
    capacity_reservation_preference = "open"
  }

  credit_specification {
    cpu_credits = "standard"
  }

  disable_api_termination = false

  ebs_optimized = true

  elastic_gpu_specifications {
    type = "test"
  }

  elastic_inference_accelerator {
    type = "eia1.medium"
  }

  iam_instance_profile {
    name = "test"
  }

  image_id = "ami-test"

  instance_initiated_shutdown_behavior = "terminate"

  instance_market_options {
    market_type = "spot"
  }

  instance_type = "t2.micro"

  kernel_id = "test"

  key_name = "test"

  license_specification {
    license_configuration_arn = "arn:aws:license-manager:eu-west-1:123456789012:license-configuration:lic-0123456789abcdef0123456789abcdef"
  }

  monitoring {
    enabled = true
  }

  network_interfaces {
    associate_public_ip_address = true
  }

  placement {
    availability_zone = "us-west-2a"
  }

  ram_disk_id = "test"

  tag_specifications {
    resource_type = "instance"

    tags = {
      Name = "test"
    }
  }

  user_data = ""
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
