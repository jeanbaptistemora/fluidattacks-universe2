resource "aws_ecs_task_definition" "main" {
  family                   = "schedule"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"

  task_role_arn      = data.aws_iam_role.prod_common.arn
  execution_role_arn = data.aws_iam_role.prod_common.arn

  cpu    = 2048
  memory = 4096

  container_definitions = jsonencode(
    [
      {
        name   = "makes"
        image  = "ghcr.io/fluidattacks/makes:22.05"
        cpu    = 2048
        memory = 4096

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
