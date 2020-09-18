resource "aws_subnet" "skims_batch_subnet" {
  availability_zone = "${var.region}a"
  cidr_block = "192.168.8.0/24"
  map_public_ip_on_launch = true
  vpc_id = var.batch_vpc_id
}

resource "aws_iam_role" "skims_ecs_instance_role" {
  name = "skims_ecs_instance_role"

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
  depends_on = [aws_iam_role_policy_attachment.skims_aws_batch_service_role]
  service_role = aws_iam_role.skims_aws_batch_service_role.arn
  state = "ENABLED"
  type = "MANAGED"

  compute_resources {
    allocation_strategy = "SPOT_CAPACITY_OPTIMIZED"
    instance_role = aws_iam_instance_profile.skims_ecs_instance_role.arn
    instance_type = [
      "optimal",
    ]
    # If a job requires `x` vcpus then at most `max_vcpus / x` jobs would run simultaneosly.
    # This parameter should be tuned so the vcpus and memory per job coincides
    #   with the launched instance
    max_vcpus = 32
    min_vcpus = 0
    security_group_ids = [
      aws_security_group.skims_aws_batch_compute_environment_security_group.id,
    ]
    subnets = [
      aws_subnet.skims_batch_subnet.id,
    ]
    tags = {
      Product = "Skims"
    }
    type = "SPOT"
  }
}

resource "aws_batch_job_queue" "skims" {
  compute_environments = [
    aws_batch_compute_environment.skims.arn,
  ]
  name = "skims"
  priority = 1
  state = "ENABLED"
}

resource "aws_batch_job_definition" "skims" {
  name = "skims"
  type = "container"

  # Thid can be overriden on a per-job basis so let's add default values
  container_properties = jsonencode({
    command = ["./build.sh", "--help"]
    image = "registry.gitlab.com/fluidattacks/product/bin:latest"
    memory = 512
    vcpus = 1
  })
}
