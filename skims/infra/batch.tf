resource "aws_subnet" "skims_batch_subnet" {
  availability_zone = "${var.region}a"
  cidr_block = "192.168.8.0/24"
  map_public_ip_on_launch = true
  vpc_id = var.batch_vpc_id
}

resource "aws_iam_role" "skims_ecs_instance_role" {
  name = "skims_ecs_instance_role"

  assume_role_policy = <<EOF
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

resource "aws_iam_role_policy_attachment" "skims_ecs_instance_role" {
  role = aws_iam_role.skims_ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "skims_ecs_instance_role" {
  name = "skims_ecs_instance_role"
  role = aws_iam_role.skims_ecs_instance_role.name
}

resource "aws_iam_role" "skims_aws_batch_service_role" {
  name = "skims_aws_batch_service_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "batch.amazonaws.com"
      }
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "skims_aws_batch_service_role" {
  role = aws_iam_role.skims_aws_batch_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_security_group" "skims_aws_batch_compute_environment_security_group" {
  name = "skims_aws_batch_compute_environment_security_group"
  vpc_id = var.batch_vpc_id

  # AWS manage this things and it's unknown what source port, protocol or ip
  # will access the machine
  ingress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_batch_compute_environment" "skims" {
  compute_environment_name = "skims"
  service_role = aws_iam_role.skims_aws_batch_service_role.arn
  type         = "MANAGED"
  depends_on   = [aws_iam_role_policy_attachment.skims_aws_batch_service_role]

  compute_resources {
    instance_role = aws_iam_instance_profile.skims_ecs_instance_role.arn
    instance_type = [
      "optimal",
    ]
    max_vcpus = 2
    min_vcpus = 0
    security_group_ids = [
      aws_security_group.skims_aws_batch_compute_environment_security_group.id,
    ]
    subnets = [
      aws_subnet.skims_batch_subnet.id,
    ]
    type = "EC2"
  }
}

resource "aws_batch_job_queue" "skims" {
  name     = "skims"
  state    = "ENABLED"
  priority = 1
  compute_environments = [
    aws_batch_compute_environment.skims.arn,
  ]
  depends_on = [aws_batch_compute_environment.skims]
}

resource "aws_batch_job_definition" "skims" {
  name = "skims"
  type = "container"

  container_properties = <<EOF
{
  "image": "registry.gitlab.com/fluidattacks/product/bin:latest",
  "memory": 1024,
  "vcpus": 1,
  "command": [
    "./build.sh",
    "--help"
  ]
}
EOF
}
