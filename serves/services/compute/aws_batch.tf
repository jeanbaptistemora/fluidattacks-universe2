resource "aws_subnet" "default" {
  availability_zone = "${var.region}a"
  cidr_block = "192.168.8.0/23"
  map_public_ip_on_launch = true
  vpc_id = var.batch_vpc_id
}

resource "aws_iam_role" "aws_ecs_instance_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
  name = "aws_ecs_instance_role"
}

resource "aws_iam_role_policy_attachment" "aws_ecs_instance_role" {
  role = aws_iam_role.aws_ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "aws_ecs_instance_role" {
  name = "aws_ecs_instance_role"
  role = aws_iam_role.aws_ecs_instance_role.name
}

resource "aws_iam_role" "aws_batch_service_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "batch.amazonaws.com"
      }
    }]
  })
  name = "aws_batch_service_role"
}

resource "aws_iam_role_policy_attachment" "aws_batch_service_role" {
  role = aws_iam_role.aws_batch_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_security_group" "aws_batch_compute_environment_security_group" {
  name = "aws_batch_compute_environment_security_group"
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

resource "aws_batch_compute_environment" "default" {
  compute_environment_name = "default"
  depends_on = [aws_iam_role_policy_attachment.aws_batch_service_role]
  service_role = aws_iam_role.aws_batch_service_role.arn
  state = "ENABLED"
  type = "MANAGED"

  compute_resources {
    allocation_strategy = "SPOT_CAPACITY_OPTIMIZED"
    instance_role = aws_iam_instance_profile.aws_ecs_instance_role.arn
    instance_type = [
      "optimal",
    ]
    max_vcpus = 32
    min_vcpus = 0
    security_group_ids = [
      aws_security_group.aws_batch_compute_environment_security_group.id,
    ]
    subnets = [
      aws_subnet.default.id,
    ]
    type = "SPOT"
  }
}

resource "aws_batch_job_queue" "default" {
  compute_environments = [
    aws_batch_compute_environment.default.arn,
  ]
  name = "default"
  priority = 1
  state = "ENABLED"
}

resource "aws_batch_job_definition" "default" {
  name = "default"
  type = "container"

  # This can be overridden on a per-job basis so let's add default values
  container_properties = jsonencode({
    command = ["./build.sh", "--help"]
    image = "registry.gitlab.com/fluidattacks/product/bin:latest"
    memory = 512
    vcpus = 1
  })
}
