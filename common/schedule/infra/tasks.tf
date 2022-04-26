resource "aws_security_group" "main" {
  name   = "schedule"
  vpc_id = data.aws_vpc.main.id

  # It is unknown what source port, protocol or ip
  # will access the machine
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name"               = "schedule"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_cloudwatch_event_rule" "main" {
  for_each = local.schedules

  name                = "schedule_${each.key}"
  is_enabled          = each.value.enabled
  schedule_expression = each.value.schedule_expression

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_ecs_task_definition" "main" {
  for_each = local.schedules

  family                   = "schedule_${each.key}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"

  task_role_arn      = data.aws_iam_role.prod_common.arn
  execution_role_arn = data.aws_iam_role.prod_common.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  cpu    = each.value.cpu
  memory = each.value.memory
  ephemeral_storage {
    size_in_gib = each.value.storage
  }

  container_definitions = jsonencode(
    [
      {
        name    = "makes"
        image   = "ghcr.io/fluidattacks/makes:22.05"
        command = each.value.command

        cpu    = each.value.cpu
        memory = each.value.memory

        environment = [
          for k, v in each.value.environment : { name = k, value = v }
        ]

        logConfiguration = {
          logDriver = "awslogs"
          Options = {
            awslogs-region        = var.region
            awslogs-group         = aws_cloudwatch_log_group.main.name
            awslogs-stream-prefix = "schedule"
          }
        }
      }
    ]
  )

  tags = {
    "Name"               = "schedule"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}


resource "aws_cloudwatch_event_target" "main" {
  for_each = local.schedules

  target_id = each.key
  rule      = aws_cloudwatch_event_rule.main[each.key].name
  arn       = aws_ecs_cluster.main.arn
  role_arn  = data.aws_iam_role.prod_common.arn

  ecs_target {
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.main[each.key].arn
    launch_type         = "FARGATE"
    propagate_tags      = "TASK_DEFINITION"

    network_configuration {
      subnets          = [data.aws_subnet.common.id]
      security_groups  = [aws_security_group.main.id]
      assign_public_ip = true
    }

    tags = {
      "Name"               = each.key
      "management:area"    = "cost"
      "management:product" = "common"
      "management:type"    = "product"
    }
  }
}
