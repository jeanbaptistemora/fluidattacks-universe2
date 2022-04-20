resource "aws_iam_role" "aws_ecs_instance_role" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      }, {
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "spotfleet.amazonaws.com"
      }
    }]
  })
  name = "aws_ecs_instance_role"

  tags = {
    "Name"               = "aws_ecs_instance_role"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_iam_role_policy_attachment" "aws_ecs_instance_role" {
  role       = aws_iam_role.aws_ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_role_policy_attachment" "aws_ecs_instance_role_fleet_tagging" {
  role       = aws_iam_role.aws_ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2SpotFleetTaggingRole"
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

  tags = {
    "Name"               = "aws_batch_service_role"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_iam_role_policy_attachment" "aws_batch_service_role" {
  role       = aws_iam_role.aws_batch_service_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}
